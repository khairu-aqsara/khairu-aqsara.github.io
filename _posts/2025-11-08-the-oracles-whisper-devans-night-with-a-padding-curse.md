---
layout: post
title: "The Oracle's Whisper: Devan's Night With a Padding Curse"
subtitle: "A young hacker, a stubborn ciphertext, and the art of listening to errors"
date: 2025-11-08 00:00:00 +0700
categories: [tech, security, cryptography]
tags: [ctf, crypto, padding-oracle, pkcs7, cbc, python]
author: Kuli Kode
---

The laptop fan was a low, steady hum—the soundtrack to Devan’s small wars. The CTF timer glowed red in the corner of the screen, eating minutes the way a black hole eats light. Empty coffee cups patrolled the desk. The room smelled faintly of rain and the metallic nostalgia of sleepless keyboards.

He tugged his hoodie tighter as the challenge page reloaded. One input box. One button. One judgment.

> "Invalid padding."
>
> Two words. A whisper. An oracle.

He didn’t know it yet, but the error message was a door. And doors, in cryptography, swing both ways.

## Chapter 1: The Clean Room and the Messy World

The challenge description was deceptively simple:

- Endpoint: `POST /api/decrypt` with JSON `{ token: <hex> }`
- Response: 200 OK with plaintext, or 400 with an error message
- Hint: "It’s all about the endings."

Devan tried the obvious. He sent the provided token. Sometimes he got `Invalid padding`. Sometimes he got `Decryption failed`. Occasionally, a `Too short`—a small scolding for malformed input.

On the wall, a whiteboard with permanent marker scars bore three words he’d written months ago: "Assume structure exists." It was the only lesson that survived his early months of brute force.

He scribbled on paper:

- AES-CBC? Likely.
- PKCS#7 padding? The error names smell like it.
- "Endings" = padding bytes at the end of the plaintext.

He remembered a talk: block ciphers are deterministic in their building blocks, but we stack them to make them practical. CBC chains blocks by XORing with the previous ciphertext. It’s safe—until the app starts gossiping about padding.

### A tiny map of CBC

```
Plain:   P1      P2      P3
Key:     K
IV:      IV

Encrypt:
C1 = E( K, P1 XOR IV )
C2 = E( K, P2 XOR C1 )
C3 = E( K, P3 XOR C2 )

Decrypt:
P1 = D(K, C1) XOR IV
P2 = D(K, C2) XOR C1
P3 = D(K, C3) XOR C2
```

With PKCS#7, padding fills the final block with N bytes, each byte equal to N. If the last byte is 0x04, the last four bytes must all be 0x04. Any mismatch? Boom—`Invalid padding`.

On his desk, a photo in a cracked frame: Devan at fifteen, his mother holding a birthday cake with too many candles for a rented apartment. She had scribbled a message on the back: "Belajar pelan-pelan, tapi jangan berhenti." Learn slowly, but don’t stop. He put the photo upright. He’d need that voice tonight.

## Chapter 2: The First, Wrong Fight

He brute-forced the keyspace of a toy cipher (because denial is a phase). He flipped random bits and prayed (because magical thinking is part of grief). He asked the challenge for sympathy. It responded with cold precision.

Another whisper: `Invalid padding.`

He laughed without humor. "Okay. You don’t guess the password. You listen to the oracle."

He felt the tension in his shoulders loosen, just a fraction. This wasn’t about muscle. It was about posture.

## Chapter 3: The Oracle Pattern (And the Fear of the Void)

He drew the classic padding-oracle pattern on his notebook—crooked, smudged, but enough to be dangerous.

- You have a ciphertext: `IV | C1 | C2 | ... | Cn`
- You want `P(n)`, the plaintext of the last block.
- You control a forged previous block `C(n-1)'`
- Send `C(n-1)' | Cn` to the server
- If padding is valid, you learned a bit about `P(n)`.

Why it works: On decryption, the server computes `D(K, Cn) XOR C(n-1)'` and then checks PKCS#7 on the result. If the last byte passes as `0x01`, you’ve aligned the stars. With enough oracle queries, you discover every byte.

He wrote the heart of the method in big, block letters:

```
Goal: Find intermediate value I = D(K, Cn)
Fact: P = I XOR C(n-1)
Trick: Force padding = k at position i, leak I[i]
```

But in the quiet between keystrokes, fear crept in. What if the challenge was a decoy? What if it wasn’t padding at all, but a timing mirage? His mind spiraled into maybes.

He opened the team chat. Only one green dot: Mira, the teammate who collected failures like data points and brewed tea that tasted like discipline.

Mira: Think like a river. Don’t fight rocks, flow around them.

Devan: What if it’s not a rock? What if it’s a cliff?

Mira: Then use a rope. Instrument it.

## Chapter 4: Building the Knife

He scaffolded the exploit in Python, his fingers finally matching his pulse.

```python
import os
import binascii
import requests
import time
from statistics import median

URL = "https://challenge.example/api/decrypt"

# Baseline classification of responses by content and timing

def oracle_raw(token_hex: str):
    t0 = time.perf_counter()
    r = requests.post(URL, json={"token": token_hex}, timeout=5)
    dt = (time.perf_counter() - t0) * 1000
    text = ""
    try:
        text = r.json().get("error", "")
    except Exception:
        text = r.text
    return r.status_code, text, dt


def is_padding_error(status, text):
    return status == 400 and ("Invalid padding" in text or "padding" in text.lower())


def is_length_error(status, text):
    return status == 400 and ("Too short" in text or "length" in text.lower())


def oracle(token_hex: str) -> bool:
    status, text, dt = oracle_raw(token_hex)
    if status == 200:
        return True
    if is_length_error(status, text):
        return False
    # If the service masks messages, use timing bands
    # We'll treat very short responses as padding rejects, longer as deeper processing
    return not is_padding_error(status, text)


def blocks(raw: bytes, size=16):
    return [raw[i:i+size] for i in range(0, len(raw), size)]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def confirm_padding(forged: bytes) -> bool:
    h = binascii.hexlify(forged).decode()
    # Primary check
    if not oracle(h):
        return False
    # Secondary negative check to filter coincidences
    test = bytearray(forged)
    test[-2] ^= 1  # disturb penultimate byte to break structured pad
    return not oracle(binascii.hexlify(bytes(test)).decode())


def attack(cipher_hex: str, block_size=16):
    ct = binascii.unhexlify(cipher_hex)
    bs = block_size
    blks = blocks(ct, bs)
    if len(blks) < 2:
        raise ValueError("Need at least IV + 1 block")

    recovered = b""

    for bi in range(len(blks)-1, 0, -1):
        prev = bytearray(blks[bi-1])
        curr = blks[bi]
        inter = bytearray(bs)  # D(K, curr)
        plain = bytearray(bs)

        for pad in range(1, bs+1):
            i = bs - pad
            # Set tail to enforce pad value across j > i
            for j in range(bs-1, i, -1):
                prev[j] = inter[j] ^ pad

            found = False
            # Heuristic: try likely ASCII first to save time
            guesses = list(range(256))
            likely = list(b" etaoinshrdlcumwfgypbvkjxqz{}_:-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            ordered = list(dict.fromkeys(likely + guesses))

            for guess in ordered:
                orig = prev[i]
                prev[i] = guess
                forged = bytes(prev) + curr
                if confirm_padding(forged):
                    inter[i] = guess ^ pad
                    plain[i] = inter[i] ^ blks[bi-1][i]
                    found = True
                    break
                prev[i] = orig

            if not found:
                # Fallback sweep without heuristics
                for guess in range(256):
                    prev[i] = guess
                    forged = bytes(prev) + curr
                    if confirm_padding(forged):
                        inter[i] = guess ^ pad
                        plain[i] = inter[i] ^ blks[bi-1][i]
                        found = True
                        break
                if not found:
                    raise RuntimeError(f"Failed at block {bi}, offset {i}")

        recovered = plain + recovered
        print(f"[+] Recovered block {bi}: {plain}")

    return recovered
```

He paused. The `oracle` assumed the server’s honesty. That’s a gift in CTFs, but in the wild the oracle might be timing-based. He added a comment to future-Devan:

> In production, error messages lie. When the text lies, the clock—and cache—tell the truth. Measure, median, mask jitter.

He looked at the timer. 06:12:35 left. His heart started to hear its own rhythm.

## Chapter 5: The Long Night of False Positives

Everything worked—until it didn’t. The last byte sang immediately. The next one refused.

False positives. The worst kind of hope.

Some guesses returned `200 OK`, but the plaintext smelled wrong: control characters in the middle of a JSON, nonsensical bytes before a colon. He remembered a painful truth: valid padding doesn’t mean valid message. Sometimes the last two bytes just happen to form `0x02 0x02` by chance. You need a second confirmation.

He hardened the check. Then he did something he’d learned from breaking rate-limited login forms: he slowed down. He randomized guesses for each byte, added tiny sleeps, and rotated User-Agents. Not for stealth, but for stability; noisy networks can turn truth into dice.

He also started keeping a small diary in the terminal:

```
[01:13] pad=01 at i=15 -> OK after 7 tries
[01:19] pad=02 at i=14 -> false positive; neg-check failed
[01:24] pad=02 at i=14 -> OK after heuristic ASCII
```

The act of recording settled his hands. He could feel the cliff become a slope.

## Chapter 6: The Turning of the Wheel

Byte by byte, the plaintext unfolded. Names, commas, a secret that looked like a session token. Then a flag fragment: `CTF{cbc_`.

His hands trembled. He slowed down—not from fear, but reverence. He had forced the oracle to speak, but the power was in the listening.

He thought of his mother’s note. "Learn slowly, but don’t stop." He let the words become a metronome between queries.

## Chapter 7: When Oracles Hide Behind Time

Halfway through the penultimate block, the messages changed. The server began returning a single, generic error: `Bad request`. No more `Invalid padding`. The chat fed a rumor: the challenge authors had toggled a patch to normalize responses.

Panic is a shape-shifter. It can look like anger. Or silence.

Devan breathed, then instrumented. He sent the same forged block fifty times, then a block with a single-byte change fifty times. The first series clustered around 18ms. The second around 24ms.

He sketched a mental model:

- Padding failure path returns early: decrypt + check last byte -> reject
- Valid padding path goes deeper: checks entire pad, maybe touches JSON parsing -> longer

He wrote a tiny timing harness.

```python
def oracle_timing(token_hex: str, trials=7) -> bool:
    times = []
    ok = 0
    for _ in range(trials):
        status, text, dt = oracle_raw(token_hex)
        times.append(dt)
        ok += 1 if status == 200 else 0
    # Treat longer median as "deeper processing" -> likely valid pad
    m = median(times)
    return ok > 0 or m > 21.0  # threshold tuned empirically
```

He swapped `oracle` for `oracle_timing` inside `confirm_padding`. The needle moved again. The oracle hadn’t vanished—it had learned to whisper through the wall. He learned to put his ear to it.

## Chapter 8: The Kitchen Table Theory of Crypto

He got up to stretch and found himself staring at the kitchen table—a cheap rectangle of fake wood that had hosted every version of "almost enough." He spilled noodles there when the internet cut out in the rain. He soldered a broken headphone wire there when he had to choose between noise and hunger. He studied CBC there, one block at a time, like laying down floor tiles.

CBC is a kitchen table cipher, he realized. You don’t need elegance. You need patience. You lay a block. Then another. If one is crooked, the next one will show it. The art is in the joints.

He laughed—a quiet, good sound. Then he sat down again.

## Chapter 9: The Knife Gets a Handle (Engineering the Exploit)

He refactored his script like a carpenter rehanging a door: fewer squeaks, more purpose.

- Extracted a `ByteRecoverer` with stateful retries and jitter
- Added a "known-plaintext" filter to prefer ASCII ranges where applicable
- Logged intermediate values `I[i]` as well as `P[i]` to debug collisions

```python
class BlockRecoverer:
    def __init__(self, bs=16):
        self.bs = bs

    def recover_block(self, prev_blk: bytes, curr_blk: bytes) -> bytes:
        prev = bytearray(prev_blk)
        inter = bytearray(self.bs)
        plain = bytearray(self.bs)

        for pad in range(1, self.bs+1):
            i = self.bs - pad
            for j in range(self.bs-1, i, -1):
                prev[j] = inter[j] ^ pad

            found = False
            for guess in range(256):
                orig = prev[i]
                prev[i] = guess
                forged = bytes(prev) + curr_blk
                if confirm_padding(forged):
                    inter[i] = guess ^ pad
                    plain[i] = inter[i] ^ prev_blk[i]
                    print(f"    [pad={pad:02d}] I[{i}]={inter[i]:02x} P[{i}]={plain[i]:02x}")
                    found = True
                    break
                prev[i] = orig

            if not found:
                raise RuntimeError(f"No guess at offset {i}")
        return bytes(plain)
```

He wrapped it with a controller that moved across blocks, left to right and back again if something smelled off. He wasn’t just writing an exploit anymore. He was composing a conversation—polite, persistent, pointed.

## Chapter 10: The Flag Isn’t the Ending

The full string materialized slowly, like a photograph in developer fluid:

```
CTF{cbc_padding_is_only_silent_until_it_screams}
```

He copied it without ceremony. The scoreboard blinked, then jumped his team up eight places. The chat filled with emojis and Mira’s laconic, perfect message:

Mira: Tea?

He stared at the flag, then at the photo of the cake. He felt the shape of something settle inside him—not pride, exactly. More like alignment. The problem and the human had finally agreed on a boundary.

## Chapter 11: What Devan Learned (So You Don’t Suffer Blindly)

- Padding-oracle vulnerabilities are not about breaking AES—they’re about abusing the interface around it. The crypto is sound; the glue is not.
- Error messages are side channels. If the text is hidden, measure time, size, or network differences. Median beats mean; bins beat wishes.
- Confirm your padding guess. Use a strict oracle to avoid false positives. Break the pad intentionally on a neighbor byte.
- Separate concerns in code: intermediate value first (I = D(K, C)), then derive plaintext (P = I XOR C_prev). Log both when debugging.
- Heuristics help but don’t decide. Prioritize sensible ASCII for speed; always fall back to full space.
- Rate limits and jitter matter. Add retries, randomize probe order, implement backoffs, and beware CDN caches.
- Ethics matter. This skill is for defense, audits, and CTF arenas. Shut real oracles up: authenticate before decrypting (Encrypt-then-MAC) or use AEAD (AES-GCM/ChaCha20-Poly1305).

## Chapter 12: Edge Cases, Pitfalls, and the Subtle Cracks

- Accidental pad collisions: A valid `0x02 0x02` can occur by chance. Always double-check by perturbing another byte.
- Full-block pad: If the last block is entirely `0x10` for 16-byte blocks, your first success might be fake. Validate with multiple neighbors.
- IV handling: If IV is user-controlled, the first block is a snack. If it’s fixed or prepended, adjust indexing carefully.
- UTF-8 traps: Don’t overfit to printable ASCII. UTF-8 multi-byte sequences can look like garbage until complete.
- WAFs and middleboxes: Some proxies buffer or normalize errors. Carry a timing harness as a first-class tool.
- TLS record effects: Chunking can smear timing. Use more samples and median-of-medians.
- Stateful sessions: Servers that bind tokens to sessions break parallelism. Throttle politely; don’t burn the oracle.

## Chapter 13: How to Fix the Real System

If you’re a builder reading this because your logs whispered back at an attacker:

- Don’t leak padding errors. Return a single generic failure message and unify timing.
- Prefer AEAD. Let the MAC authenticate the entire ciphertext and associated data before any decryption logic.
- If you must use CBC+PKCS#7, verify a MAC first (EtM), and run padding checks in constant time.
- Use constant-time compares for MACs. Don’t write your own; most standard libs got this right so you don’t have to.
- Log carefully: sensitive exceptions should be rate-limited and scrubbed. Don’t turn logs into oracles.

### A minimal EtM sketch

```python
# Pseudocode

msg = iv || ciphertext
if not verify_hmac(msg, tag, key_mac):
    return error_generic()
plaintext = cbc_decrypt(ciphertext, key_enc, iv)
return ok(plaintext)
```

### A test harness mindset

- Build a small local oracle service that mimics your app’s patterns.
- Add toggles for "verbose errors" vs "generic" and measure the difference.
- Record distributions, not anecdotes. If you’re not charting, you’re guessing.

## Chapter 14: The Morning After (And the Real Win)

He logged off the scoreboard and closed the tabs. The room felt bigger, as if the walls had moved back an inch. Outside, dawn pushed through the blinds in thin silver spears.

He washed the coffee mug and put it down with a care that bordered on tenderness. He texted his mother a photo of the flag. She replied with a voice note—sleep in her voice, pride in the edges.

"Pelan-pelan saja, Van. Yang penting, jangan berhenti."

Slowly is fine. What matters is: don’t stop.

He realized the CTF hadn’t taught him how to break AES. It taught him how to be patient with problems that don’t care about him. It taught him that most systems fail in the seams and that most victories come from listening where others shout.

He didn’t feel like a hero. He felt like a locksmith who finally learned to listen for the quiet click.

## Key Takeaways (for Skimmers)

- CBC padding oracles leak through messages or time; treat both as channels.
- Confirm padding with a negative test; false positives are ambush predators.
- Instrument first, code second. Your exploit is a measurement device.
- Fix with AEAD or Encrypt-then-MAC; unify errors and timing.
- Respect rate limits and ethics. Curiosity is a craft, not a costume.

## Epilogue: The Oracle’s Last Whisper

Weeks later, Devan would stumble across a job posting that asked for "experience with side-channel attacks." He would attach this write-up—not the flag, but the thoughtfulness between the lines. Interviews would follow. Some would ask him to whiteboard; a few would ask him to explain how he knew the difference between coincidence and signal.

He would tell them about a night when time became language and error messages became wind chimes. He would tell them about patience that wasn’t passive and confidence that wasn’t loud. He would tell them about a photograph in a cracked frame and a sentence on a whiteboard.

Assume structure exists.

And then, find it.
