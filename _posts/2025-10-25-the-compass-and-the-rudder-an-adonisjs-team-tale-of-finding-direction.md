---
layout: post
title: "The Compass and The Rudder: An AdonisJS Team's Tale of Finding Direction"
subtitle: "When 'Lead' is a title, but leadership is a role nobody owns"
date: 2025-10-25 09:00:00 +0700
categories: [tech, software-development, team-dynamics]
tags: [adonisjs, project-management, tech-lead, leadership, teamwork, software-engineering]
author: Kuli Kode
---

The project kickoff felt like the first day of a road trip. The map was fresh, the tank was full, and the destination—a sleek, modern web application—gleamed on the horizon. Our vehicle of choice was AdonisJS, a Node.js framework that felt like a luxury sedan: powerful, elegant, and a joy to drive. At the wheel was Khairu, our newly appointed "Project Lead." The mood was electric, buzzing with the kind of optimism that only exists before the first line of code is written. What could possibly go wrong?

Everything. Everything could go wrong.

## Chapter 1: The Smooth Open Road

Our team was a solid mix, each of us bringing a unique energy. Devan, our most seasoned backend developer, had spent the weekend poring over the AdonisJS documentation. He was practically vibrating with excitement to implement its elegant IoC container and the Lucid ORM. Myesha, with her unwavering focus on user experience, was already sketching out user flows, her mind dedicated to ensuring we built something people would not just use, but love. Jovian and Fitriyana, two bright and eager developers, were ready to absorb everything and code their hearts out.

And then there was Khairu. Sharp, organized, and universally respected. Management had given him the title of "Project Lead," a promotion he had worked hard for and deeply desired. His first act was to present a beautifully crafted project plan. The Gantt chart wasn't just a series of bars on a screen; it was a work of art, a symphony of dependencies and timelines that promised a smooth, predictable journey.

"Team, this is our roadmap to success," he announced, his voice resonating with pride. "Every feature is broken down, every milestone is clear. If we stick to this, we'll deliver on time and under budget. Let's build something incredible."

We all cheered, caught up in his confidence. The road ahead looked smooth, straight, and paved with gold.

> "A goal without a plan is just a wish." — Antoine de Saint-Exupéry
>
> *What he didn't mention is that a plan without clear roles is a roadmap to a traffic jam.*

## Chapter 2: The First Wrong Turn

The first sprint began, and the initial harmony started to fray. Devan, tasked with setting up the core application structure, was in his element, practicing the software craftsmanship he so deeply believed in. He was meticulously crafting service providers, defining clear interfaces, and using the IoC container to ensure our architecture was clean, testable, and scalable from day one.

```typescript
// Devan's "build it right" approach
// app/providers/SearchServiceProvider.ts
import { ApplicationContract } from '@ioc:Adonis/Core/Application'

export default class SearchServiceProvider {
  constructor(protected app: ApplicationContract) {}

  public register() {
    // Bind our SearchService implementation to the IoC container
    this.app.container.singleton('App/Services/SearchService', () => {
      const esConfig = this.app.config.get('elasticsearch')
      const client = new ElasticsearchClient(esConfig)
      // This service will be beautifully decoupled and easily mockable for tests
      return new SearchService(client)
    })
  }
}
```

He was building a cathedral. Then Khairu came over, his brow furrowed with the distinct anxiety of someone staring at a calendar.

"Devan, this is elegant, I get it. But it's taking too long," Khairu said, his voice a low, urgent whisper. "The stakeholder demo is in two weeks. We need to show them a working search endpoint, not a perfect service provider. Can't we just put the Elasticsearch client logic directly in the controller for now? We can refactor it later."

Devan’s fingers froze over his keyboard. He felt a flush of frustration. *Doesn't he see?* he thought. *'Later' is a lie we tell ourselves. This is the foundation. If we build on sand, the whole thing will collapse under its own weight.*

"Refactor later? Khairu, you know that's a debt we'll never repay," Devan said, trying to keep his voice even. "This is the foundation. It has to be solid."

Khairu’s jaw tightened. *Doesn't he see the pressure I'm under?* he thought, the faces of the stakeholders flashing in his mind. *They don't care about dependency injection. They care about the demo. My neck is on the line if we have nothing to show.*

"It's not sand, it's a calculated shortcut," Khairu countered. "I'm managing the timeline. We need to show progress, not architectural purity."

Devan saw a future of spaghetti code and late-night debugging sessions. Khairu saw a future of missed deadlines and angry emails from management. They were both trying to do what was best for the project, but their definitions of "best" were worlds apart. Fitriyana, who was waiting to build the search feature, stood by awkwardly, caught in the crossfire, holding two conflicting sets of instructions. The smooth road ahead had just revealed its first, jarring pothole.

## Chapter 3: The Two-Headed Dragon

The initial harmony was officially over. The office, once buzzing with collaborative energy, grew quiet. Headphones became shields. Conversations became transactional. The confusion began to bleed into every aspect of the project, with Khairu as its unwilling epicenter—a two-headed dragon pulling the team in opposite directions.

**In the morning, he was the Project Manager.** He’d call a stand-up, his eyes fixed on his digital project board. "Fitriyana, the board says the login ticket is at 80%. The deadline is EOD. What's the blocker?" His focus was relentlessly on the *what* and the *when*.

**In the afternoon, he was the Tech Lead.** He’d dive into a pull request from that same login ticket and leave a dozen comments on coding style and implementation details. "We should use a different hashing algorithm here for better security," he’d write, directly contradicting the approach Devan had laid out for the team. His focus was on the *how*.

The whiplash was giving everyone vertigo. One afternoon, the tension boiled over. During a daily stand-up, Fitriyana gave her update. "I've implemented the password reset flow as Devan architected, using a queued job for sending emails."

Devan nodded in approval. But before he could speak, Khairu interjected. "A queue? That's overkill. We need this done by tomorrow. Just send the email directly in the controller. It's faster to implement."

The entire team froze. Fitriyana's face turned red. She was being given conflicting orders from her two "bosses" in front of everyone. She looked from Khairu to Devan, her expression pleading for a single source of truth that didn't exist. The silence was deafening.

We weren't a team anymore. We were a group of individuals taking orders from two different bosses who just happened to be the same person.

> "If you have more than one person telling you how to do the same thing, you don't have a leader. You have a problem." — A wise, and probably very tired, developer.

## Chapter 4: The Heart of the Conflict

The core of our struggle manifested in our beautiful AdonisJS codebase, which was slowly turning into a Frankenstein's monster—a patchwork of elegant architecture and hasty shortcuts.

Devan, acting as the de-facto Tech Lead, championed using AdonisJS to its full potential. His vision was a symphony of best practices.

```typescript
// Devan's vision: Clean, decoupled, and testable
// app/Controllers/Http/SearchController.ts
import { inject } from '@adonisjs/core/build/standalone'
import SearchService from 'App/Services/SearchService'
import SearchValidator from 'App/Validators/SearchValidator'

@inject(['App/Services/SearchService'])
export default class SearchController {
  constructor(private searchService: SearchService) {}

  public async handle({ request }) {
    // 1. Validate input using a dedicated validator class. Clean!
    const { query } = await request.validate(SearchValidator)
    
    // 2. The controller knows NOTHING about how the search is performed.
    // It just calls the service. Beautifully decoupled.
    return this.searchService.performSearch(query)
  }
}
```

Khairu, driven by his PM-instincts for speed, pushed for a more direct—and more coupled—approach. His code wasn't bad, but it prioritized immediate results over long-term health.

```typescript
// Khairu's vision: Fast, direct, and a future maintenance nightmare
// app/Controllers/Http/SearchController.ts
import { ElasticsearchClient } from 'some-library' // Uh oh, direct dependency
import { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'

export default class SearchController {
  public async handle({ request, response }: HttpContextContract) {
    const query = request.input('q')

    // 1. Manual validation right in the controller. Messy.
    if (!query || query.length < 3) {
      return response.badRequest({ error: 'Query must be at least 3 characters.' })
    }
    
    // 2. All the logic is right here. Fast to write, impossible to test or change.
    const client = new ElasticsearchClient({ node: 'http://localhost:9200' })
    const results = await client.search({
      index: 'products',
      body: { query: { match: { title: query } } }
    })

    return results.body.hits.hits
  }
}
```

Devan saw this and felt a physical sense of despair. "We're giving up the best parts of the framework! This isn't scalable. It's not testable. We're creating technical debt before we've even launched."

Khairu, reviewing the code, saw it differently. "We're shipping features. This code works. We can fix the 'debt' after we have something to show the stakeholders."

They were both right. And that was the entire, soul-crushing problem.

## Chapter 5: The Inevitable Collision

The stakeholder demo was an unmitigated disaster. It wasn't just bad; it was a slow-motion train wreck.

Khairu, his voice betraying a confidence he didn't feel, walked the stakeholders through the app. He clicked the search bar. "And now, our powerful, real-time search..." He typed a query and hit Enter. A loading spinner appeared. And spun. And spun. The search feature, built Khairu's "fast way," was buckling under the load of the demo database.

A nervous sweat beaded on Khairu's forehead. "Just warming up the servers," he joked weakly. The stakeholders smiled polite, tight-lipped smiles that didn't reach their eyes. He quickly moved to the user authentication flow—the one Devan had been forced to rush. He tried to log in. A red banner screamed: `Cannot read property 'id' of null`. A 500 error.

The rest of the demo was a painful blur of broken features and awkward apologies.

The retrospective that afternoon was brutal. The air was thick with unspoken blame and palpable frustration. Finally, Devan couldn't hold it in any longer. "This is exactly what I warned would happen!" he burst out, his voice shaking with anger. "We took shortcuts and the bill came due!"

"And if we'd followed your 'perfect' plan, we wouldn't have even had a broken demo to show!" Khairu shot back, his own frustration and humiliation boiling over. "We'd still be configuring service providers!"

It was Myesha who finally broke the silence, her voice quiet but firm. "Stop. This isn't about shortcuts or purity. This isn't Devan's fault or Khairu's fault. It's our fault. All of us. We've been trying to sail a ship where the person holding the compass is also frantically trying to steer the rudder. We are lost because we don't know who is leading us where."

## Chapter 6: The Compass and The Rudder

That was the moment of clarity. The anger in the room subsided, replaced by a dawning, painful understanding. Khairu wasn't a bad leader; he was trying to be two leaders at once. We finally sat down to define the roles we had so desperately needed from the start.

This is what we learned, the hard way:

### The Project Manager: The Compass

The Project Manager is the guardian of the **"What"** and the **"When."** They hold the map, watch the horizon, and ensure the destination is the right one.

-   **Their Core Mission:** To deliver the right product to the right people, on time and on budget.
-   **Their Key Questions:** *Why* are we building this? *What* problem does it solve? *Who* is it for? *When* do we need it?
-   **A Day in Their Life:**
    -   Communicating progress and managing expectations with stakeholders.
    -   Clarifying requirements and writing clear, concise user stories.
    -   Identifying and mitigating risks to the project timeline or budget.
    -   Shielding the development team from scope creep and mid-sprint priority changes.
-   **Their Measure of Success:** On-time delivery, stakeholder satisfaction, and achieving the desired business outcomes.

### The Tech Lead: The Rudder

The Tech Lead is the guardian of the **"How."** They are deep in the engine room, ensuring the ship is sound, fast, and that the crew knows how to operate it.

-   **Their Core Mission:** To ensure the product is built with technical excellence, making it scalable, maintainable, and reliable.
-   **Their Key Questions:** *How* should we build this to be scalable? *How* do we ensure it's secure and performant? *How* can we improve our development process?
-   **A Day in Their Life:**
    -   Designing system architecture and making high-level technical decisions.
    -   Mentoring other developers through pair programming and constructive code reviews.
    -   Establishing and enforcing coding standards and best practices.
    -   Spiking new technologies and tackling the most complex technical challenges.
-   **Their Measure of Success:** System uptime, performance metrics, code quality, developer velocity, and team morale.

A Project Manager who dictates technical implementation creates a brittle product. A Tech Lead who ignores business goals creates a perfect product that never ships. **You need both, but you cannot confuse them.** They are two distinct, full-time jobs.

## Chapter 7: A New Course

In that meeting room, Khairu let out a long, slow breath. The defensiveness was gone, replaced by a weary acceptance. "You're right," he said, looking around the table. "I've been trying to steer and navigate at the same time. I've been a terrible 'Project Lead' because I was trying to be two things at once, and failing at both."

He looked at Devan. "Devan, you've been the real technical leader on this project from day one, even when I was fighting you. I'm making it official. You are the Tech Lead. Your word is final on *how* we build."

Then he turned to the rest of us, a new resolve in his eyes. "My job is to be the Project Manager. I will tell you *what* we need to build and *when*. And I will fight to give you the time and resources you need to do it the right way. I will be your shield."

It was like a pressure valve had been released in the soul of the team. We spent the next hour on the whiteboard, mapping our new reality.
-   **Requirement questions?** Go to Khairu.
-   **Architectural questions?** Go to Devan.
-   **Stakeholder wants a "quick change"?** They talk to Khairu, who then discusses the priority and timeline impact with Devan.

## Epilogue: Sailing True

The next sprint planning meeting was a revelation. Khairu presented the user stories, clearly defining the "what" and "why." Then he turned the floor over to Devan, who walked the team through the technical strategy, whiteboarding the "how." For the first time, there was a single, coherent plan.

Our AdonisJS app, once a source of conflict, became a joy to work on again. We were building it the right way, *and* we were hitting our deadlines. The code was clean, the features were solid, and the team was happy.

We learned that the title "Project Lead" is a trap. It's a dangerously ambiguous term that invites chaos. A team doesn't need a single, all-powerful "lead." It needs leadership. It needs a compass to set the direction and a rudder to steer the ship. And it needs to know, without a shadow of a doubt, who is holding which.