# Problem v038

The v037 scientific Candidate remains unevaluated because its capture runner
failed before subprocess launch. The concrete execution problem is that a new
Run version has no `captures` parent and the runner's single-level `mkdir()`
cannot create `captures/dev_001`.

v038 asks only whether the unchanged frozen ECDS Development execution can be
captured after correcting parent creation. It introduces no research problem,
method, data, model, gate or claim change.
