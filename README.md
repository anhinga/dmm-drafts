# dmm-drafts

Auxiliary repository for **dataflow matrix machines** experiments.

---

The main and canonical DMM repository is https://github.com/jsa-aerial/DMM

The code there is written in idiomatic Clojure, with emphasis of
programming with immutable structures friendly to parallelization.

Since DMMs are a bridge between programs and neural nets, 
the fact that the canonical implementation
is in Clojure should eventually facilitate new experiments in programming
languages based on the DMM architecture.

---

However, it seems to be desirable to also have an **auxiliary version** of DMMs in Python.

This should make possible for engineers not familiar with Clojure to experiment
with DMMs. This should also enable inclusion of DMMs into one of the machine
learning frameworks already equipped with automated differentiation, such as e.g. PyTorch.
There are a number of other cases, when an important machine learning method
is already publicly available in Python, but not yet available in Clojure.

Note than for now we are treating this repository as one intended only for
**exploratory experimentation**. If it is desirable to make this Python version
more production-like, it would be necessary to complete refactor
the code base in the present repository. Currently we don't have such plans.
