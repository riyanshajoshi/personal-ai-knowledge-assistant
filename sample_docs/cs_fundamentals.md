# CS Fundamentals: Data Structures Overview

## Arrays
An array is a collection of elements stored at contiguous memory locations, accessed by an index. Reading or writing an element by index takes constant time, since the memory address can be calculated directly. However, inserting or deleting an element in the middle of an array requires shifting subsequent elements, which takes linear time.

## Stacks
A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Elements are added and removed from the same end, called the top. Common operations are push (add an element) and pop (remove the most recently added element). Stacks are used in scenarios like function call management (the call stack), undo operations in editors, and expression evaluation.

## Queues
A queue follows the First-In-First-Out (FIFO) principle. Elements are added at the rear and removed from the front. Queues are commonly used in scheduling tasks, handling requests in the order they arrive, and breadth-first search traversal in graphs.

## Linked Lists
A linked list is a sequence of nodes, where each node contains data and a reference (or pointer) to the next node. Unlike arrays, linked lists don't require contiguous memory, which makes insertion and deletion efficient at any position, but accessing an element by index requires traversing the list from the start, taking linear time.

## Hash Tables
A hash table stores key-value pairs and uses a hash function to compute an index into an array of buckets, allowing average-case constant time lookup, insertion, and deletion. Collisions, where two keys hash to the same index, are typically handled through chaining (storing multiple entries per bucket) or open addressing (finding another open slot).

## Trees
A tree is a hierarchical data structure with a root node and child nodes, where each node can have zero or more children. A binary tree restricts each node to at most two children. Binary search trees maintain the property that left children are smaller and right children are larger than their parent, enabling efficient searching in balanced trees.

## Graphs
A graph consists of nodes (vertices) connected by edges, and can represent relationships like social networks, road maps, or dependency structures. Graphs can be directed or undirected, and weighted or unweighted. Common traversal algorithms include depth-first search and breadth-first search.