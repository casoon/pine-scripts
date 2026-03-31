# About This Collection

A mix of sketches and working tools — some of these scripts are just idea sketches that I never finished, others are functional and I still use them occasionally. The RTA libraries and strategies in particular are unfinished: I had a clear vision but didn't see them through to the end. Some scripts automate things I used to do manually on charts; others are purely experimental.

This collection was also my way of learning Pine Script. I appreciate the idea of having custom analysis tools right inside a chart, but I found Pine's limitations frustrating over time. I'm now moving toward building my own charting tools in Rust, where I have full control over the architecture.

**The idea behind all of this:** TradingView already has plenty of simple indicators. My goal was to build something more complex — not an all-in-one mega-indicator, but a set of composable building blocks. The approach: combine multiple analytical concepts, layer filters and logic on top, and gradually work toward statements that actually mean something. From there, derive strategy-level decisions — when does a signal apply, when doesn't it — and iteratively optimize toward better outcomes. The RTA libraries were meant to be the reusable foundation for that kind of work.

**Why publish these here?** My scripts were removed from TradingView publication twice. I can partly understand the moderation challenges when many people want to publish scripts — but there's a significant amount of thought and effort behind these (as the code hopefully reflects). Some of it was built with AI assistance, but the concepts, the ideas, and the overall design are mine. You don't put this kind of work in just for yourself. I wanted to find people to collaborate with, to get feedback — and when that's not possible through TradingView's publication system, there's no reason to stay on the platform.

So here they are — freely available. **None of these are polished, production-ready products.** But some can be useful as-is, and others might serve as inspiration or a starting point for your own work. Browse around, take what's useful, and feel free to build on it.
