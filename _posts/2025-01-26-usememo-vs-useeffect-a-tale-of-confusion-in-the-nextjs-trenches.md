---
layout: post
title: "useMemo vs useEffect: A Tale of Confusion in the Next.js Trenches"
subtitle: "When optimization becomes the problem, not the solution"
date: 2025-01-26 08:30:00 +0700
categories: [tech, frontend, react, nextjs]
tags: [nextjs, react, hooks, usememo, useeffect, performance, debugging]
author: Kuli Kode
---

The clock on my screen read 2:47 AM. I had been staring at the same component for three hours. My coffee had gone cold, my eyes were burning, and somewhere in the depths of this Next.js codebase, something was re-rendering. A lot.

**Welcome to the paradox of modern frontend development: the tools meant to make us faster sometimes slow us down.**

## Chapter 1: The Innocent Beginning

It started innocently enough. Product handed me a ticket: *"Dashboard is slow. Users complaining. Fix performance."*

Classic. No specifics, no reproduction steps, just the digital equivalent of "make it faster."

I opened the dashboard component. 847 lines. My heart sank.

```jsx
// The Dashboard of Doom
const Dashboard = ({ userId, filters, dateRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // And about 40 more state variables...
  // Because someone thought "one state per field" was a good idea
}
```

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler
>
> *What Martin didn't mention: most of us write code that confuses both.*

## Chapter 2: Enter the Hooks

The previous developer (who conveniently left the company two months ago) had sprinkled `useEffect` and `useMemo` throughout the code like confetti at a New Year's party. Generous, but chaotic.

```jsx
const Dashboard = ({ userId, filters, dateRange }) => {
  const [data, setData] = useState([]);
  
  // useEffect #1: Fetch data when userId changes
  useEffect(() => {
    fetchUserData(userId).then(setData);
  }, [userId]);
  
  // useEffect #2: Also fetch data when filters change
  useEffect(() => {
    if (filters) {
      fetchFilteredData(userId, filters).then(setData);
    }
  }, [filters, userId]);
  
  // useEffect #3: But wait, dateRange too!
  useEffect(() => {
    fetchDataByDateRange(userId, filters, dateRange).then(setData);
  }, [dateRange, userId, filters]);
  
  // useMemo #1: Memoize something... I think?
  const processedData = useMemo(() => {
    return data.map(item => ({
      ...item,
      formatted: formatData(item)
    }));
  }, [data]);
  
  // useMemo #2: Memoize the memoized data? Sure, why not?
  const sortedData = useMemo(() => {
    return processedData.sort((a, b) => a.date - b.date);
  }, [processedData]);
  
  // More memoization because performance!
  const filteredSortedProcessedData = useMemo(() => {
    return sortedData.filter(item => item.active);
  }, [sortedData]);
  
  return (
    <div>
      {/* Component that re-renders 47 times on mount */}
    </div>
  );
}
```

I ran the profiler. The component was rendering **47 times** on initial load.

*Forty. Seven. Times.*

## Chapter 3: The Great Confusion

Here's what they don't tell you in tutorials: **`useMemo` and `useEffect` solve completely different problems, but they look similar enough to confuse the hell out of you at 3 AM.**

Let me break down my confusion:

### The useEffect Spiral

**What I thought useEffect did:**
"It runs my code when dependencies change. Easy!"

**What useEffect actually does:**
"It runs your side effects after render, creating a whole new lifecycle you need to manage, and if you're not careful, you'll create infinite loops, race conditions, and a debugging nightmare that will haunt you for weeks."

I found this gem:

```jsx
useEffect(() => {
  // Fetch data
  const newData = fetchData(userId);
  setData(newData); // This triggers a re-render
}, [data, userId]); // And since data changed, this runs again
// Congratulations, you've created an infinite loop!
```

**The kuli-kode's lament:** I spent 45 minutes debugging why the API was being called thousands of times, slowly draining our API quota and probably waking up someone on the ops team.

### The useMemo Mystery

**What I thought useMemo did:**
"It makes things faster by caching calculations. I should use it everywhere!"

**What useMemo actually does:**
"It memoizes the *result* of a calculation to avoid expensive re-computations, but if you use it wrong, you're just adding overhead for no benefit."

Here's what the previous dev did:

```jsx
// Memoizing a simple string concatenation
const userName = useMemo(() => {
  return `${firstName} ${lastName}`;
}, [firstName, lastName]);

// Memoizing... a static value?
const STATIC_CONFIG = useMemo(() => {
  return { theme: 'dark', locale: 'en' };
}, []); // This defeats the entire purpose

// Memoizing something that's already fast
const isValid = useMemo(() => {
  return email.includes('@');
}, [email]);
```

**The overhead of memoization was worse than just recalculating.**

## Chapter 4: The Debugging Descent

I added console logs. Rookie move, but desperate times.

```jsx
const Dashboard = ({ userId, filters, dateRange }) => {
  console.log('Dashboard render');
  
  useEffect(() => {
    console.log('Effect 1: userId changed', userId);
  }, [userId]);
  
  useEffect(() => {
    console.log('Effect 2: filters changed', filters);
  }, [filters]);
  
  const processedData = useMemo(() => {
    console.log('Memo 1: processing data');
    return data.map(formatData);
  }, [data]);
  
  // ... more logging
}
```

My console looked like a Matrix screensaver:

```
Dashboard render
Effect 1: userId changed 123
Effect 2: filters changed {...}
Memo 1: processing data
Dashboard render
Effect 1: userId changed 123
Memo 1: processing data
Dashboard render
Dashboard render
Effect 2: filters changed {...}
Memo 1: processing data
Dashboard render
...
```

**The pattern emerged:** Objects as dependencies were being recreated on every render, triggering effects, which updated state, which triggered renders, which recreated objects...

*I was in dependency hell.*

## Chapter 5: The Moment of Clarity

At 4:23 AM, fueled by my fourth coffee and existential dread, I had an epiphany.

**The problem wasn't useMemo or useEffect. The problem was me not understanding WHEN to use each.**

### The Truth About useEffect

**Use it for:**
- Side effects (API calls, subscriptions, DOM manipulation)
- Things that happen *because* of a render
- Synchronizing with external systems

**Don't use it for:**
- Transforming data for rendering (use useMemo or just calculate it)
- Initialization that should happen once (use useState initializer)
- Creating infinite loops (obviously, but here I was)

```jsx
// WRONG: Using useEffect to transform data
useEffect(() => {
  const processed = data.map(formatData);
  setProcessedData(processed);
}, [data]); // Extra state + extra render = bad

// RIGHT: Just calculate it
const processedData = data.map(formatData);
// Or if it's expensive:
const processedData = useMemo(() => data.map(formatData), [data]);
```

### The Truth About useMemo

**Use it for:**
- Expensive calculations that slow down renders
- Preserving referential equality for dependency arrays
- Actually measurable performance problems

**Don't use it for:**
- Everything (you're not as smart as you think)
- Simple operations (string concatenation, basic math)
- Premature optimization (measure first!)

```jsx
// WRONG: Memoizing cheap operations
const fullName = useMemo(() => 
  `${firstName} ${lastName}`, 
  [firstName, lastName]
); // The memoization costs more than the operation

// RIGHT: Just do it
const fullName = `${firstName} ${lastName}`;

// WRONG: Memoizing without measuring
const sortedList = useMemo(() => 
  list.sort(), 
  [list]
); // Is this even slow?

// RIGHT: Profile first, optimize second
// If list has 1 million items, then yes, memoize
// If list has 10 items, you're wasting time
```

## Chapter 6: The Refactor

Armed with clarity and the fading hope of getting some sleep, I started refactoring.

### Before: The Chaos

```jsx
const Dashboard = ({ userId, filters, dateRange }) => {
  const [data, setData] = useState([]);
  const [processedData, setProcessedData] = useState([]);
  
  // Multiple effects fighting for control
  useEffect(() => {
    fetchUserData(userId).then(setData);
  }, [userId]);
  
  useEffect(() => {
    fetchFilteredData(userId, filters).then(setData);
  }, [filters, userId]);
  
  // Processing in effect (wrong!)
  useEffect(() => {
    setProcessedData(data.map(formatData));
  }, [data]);
  
  // Over-memoization
  const sortedData = useMemo(() => 
    processedData.sort(), 
    [processedData]
  );
  
  return <DataTable data={sortedData} />;
}
```

### After: The Clarity

```jsx
const Dashboard = ({ userId, filters, dateRange }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // ONE effect for data fetching
  useEffect(() => {
    let cancelled = false;
    
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await fetchDashboardData({
          userId,
          filters,
          dateRange
        });
        if (!cancelled) {
          setData(result);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };
    
    fetchData();
    
    return () => {
      cancelled = true; // Cleanup to prevent state updates after unmount
    };
  }, [userId, filters, dateRange]); // All dependencies, one effect
  
  // Just calculate if it's cheap
  const processedData = data.map(formatData);
  
  // Memoize only if expensive (and this is, with 10k+ items)
  const sortedAndFiltered = useMemo(() => {
    return processedData
      .filter(item => item.active)
      .sort((a, b) => a.date - b.date);
  }, [processedData]);
  
  if (loading) return <LoadingSpinner />;
  
  return <DataTable data={sortedAndFiltered} />;
}
```

**Renders on mount:** 2 (loading state + data loaded)

**API calls:** 1

**My sanity:** Partially restored

## Chapter 7: The Lessons From the Trenches

After deploying the fix (and finally getting some sleep), I documented what I learned:

### 1. **Different Tools, Different Jobs**

```jsx
// useEffect = "Do something BECAUSE render happened"
useEffect(() => {
  // API calls, subscriptions, DOM updates
  trackPageView(pageName);
  subscribeToWebSocket();
  document.title = pageTitle;
}, [dependencies]);

// useMemo = "Calculate something FOR render"
const value = useMemo(() => {
  // Transform data, expensive calculations
  return heavyComputation(rawData);
}, [rawData]);
```

### 2. **Objects and Arrays Are Liars**

```jsx
// These look the same to you, but React sees them as different
const filters = { status: 'active' }; // New object every render
const filters = { status: 'active' }; // Another new object

// This causes infinite loops:
useEffect(() => {
  doSomething(filters);
}, [filters]); // filters changes every render (in React's eyes)

// Solutions:
// A) Use primitive values
useEffect(() => {
  doSomething(status);
}, [status]); // status is a string, no problem

// B) Memoize the object
const filters = useMemo(() => ({ 
  status: 'active' 
}), []); // Now it's stable

// C) Stringify for comparison (hacky but works)
const filtersString = JSON.stringify(filters);
useEffect(() => {
  doSomething(JSON.parse(filtersString));
}, [filtersString]);
```

### 3. **Profile Before You Optimize**

I learned this the hard way. 80% of the `useMemo` calls in that codebase were useless.

```jsx
// Measure with React DevTools Profiler
// If the calculation takes < 1ms, don't memoize it
// If it takes > 10ms, memoize it
// In between? Use judgment

// The cost of memoization:
// - Memory to store the cached value
// - Comparison cost for dependencies
// - Mental overhead for developers

// Only worth it if the calculation is genuinely expensive
```

### 4. **Dependency Arrays Don't Lie (But You Might)**

```jsx
// ESLint will save your life
// Install: eslint-plugin-react-hooks

// It catches this:
useEffect(() => {
  fetchData(userId, filters);
}, [userId]); // Missing 'filters' dependency!

// And this:
const memoized = useMemo(() => {
  return calculate(a, b, c);
}, [a, b]); // Missing 'c' dependency!

// Listen to the linter. It knows.
```

### 5. **One Effect to Rule Them All**

```jsx
// WRONG: Multiple effects managing related state
useEffect(() => {
  if (userId) fetchUserData(userId);
}, [userId]);

useEffect(() => {
  if (filters) fetchFilters(filters);
}, [filters]);

useEffect(() => {
  if (userId && filters) combineData();
}, [userId, filters]);

// RIGHT: One effect, one purpose
useEffect(() => {
  const loadDashboard = async () => {
    const [userData, filterData] = await Promise.all([
      fetchUserData(userId),
      fetchFilters(filters)
    ]);
    setCombinedData(combineData(userData, filterData));
  };
  
  loadDashboard();
}, [userId, filters]);
```

## Chapter 8: The Meta-Lesson

Here's what nobody tells you about Next.js (or React, or any modern framework):

**The tools are powerful. Too powerful. And with great power comes great confusion.**

We have `useState`, `useEffect`, `useMemo`, `useCallback`, `useRef`, `useReducer`, `useContext`, `useLayoutEffect`, `useImperativeHandle`, `useDebugValue`...

Each solves a specific problem. But when you're in the trenches at 3 AM, they all blur together into a soup of "use-something-to-make-it-work."

**The real skill isn't knowing all the hooks. It's knowing which one to use and when to use none at all.**

## Chapter 9: The Morning After

I deployed the fix at 5:47 AM. The dashboard loaded in 0.8 seconds instead of 4.2 seconds. The Lighthouse score jumped from 67 to 94. The users stopped complaining.

Product sent a thumbs-up emoji. My manager said "nice work."

Nobody asked about the three useEffect calls I deleted, the seven useMemo calls I removed, or the infinite loop I prevented. Nobody knew about the 8 hours of debugging, the cold coffee, or the existential crisis about whether I actually understood React.

**That's the life of a kuli-kode.**

We dig through confusion, fight with dependencies, argue with our past selves about why we thought this was a good idea, and eventually—hopefully—make things better.

## Epilogue: The Wisdom

If you're struggling with `useMemo` and `useEffect` in your Next.js project, know this:

1. **You're not alone.** We've all been there, staring at dependency arrays at ungodly hours.

2. **Start simple.** Don't optimize until you measure. Don't memoize until you profile. Don't add effects until you need side effects.

3. **Read the docs. Again.** Seriously, the React docs on hooks are actually good. Read them when you're not panicking.

4. **Use the linter.** `eslint-plugin-react-hooks` is your friend, not your enemy.

5. **Question every hook.** Ask yourself: "Do I actually need this? Or am I cargo-culting from Stack Overflow?"

And most importantly:

6. **It's okay to be confused.** This stuff is genuinely confusing. The fact that you're trying to understand it makes you a better developer.

---

*The dashboard is fast now. The users are happy. And I finally understand the difference between calculating a value and causing a side effect.*

*Until the next ticket arrives. Then I'll probably be confused all over again.*

*But that's okay. That's what it means to be a kuli-kode in the Next.js trenches.*

---

**Got your own useMemo vs useEffect horror stories? Battle scars from the dependency array wars? Share them. We're all in this together.**

*P.S. - If you see code with 40 useEffect calls in one component, run. Just run. It's not worth it.*

---

**Resources that saved me:**

- [React Docs: useEffect](https://react.dev/reference/react/useEffect)
- [React Docs: useMemo](https://react.dev/reference/react/useMemo)
- [Kent C. Dodds: useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback)
- [Dan Abramov: A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/)
- Coffee. Lots of coffee.
