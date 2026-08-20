# Research Problem v027

In P084, keeping 200 BFCL requests fixed while adding semantically related but intended-function-different tools destabilizes function selection. A strong frozen full-schema cross-encoder still selected a non-gold function on 14/200 exposed Development rows.

The bounded question is whether decomposing each real tool schema into operation and argument views, then learning menu-relative gold-versus-distractor field differences on other query folds, improves top-1 gold-function membership and MRR over the identical full-schema cross-encoder and controls that remove either field factorization or pairwise menu-relative learning.

The setting is compact-menu function selection only. It does not evaluate argument values, complete multi-call-set recall, execution, stateful Agent behavior, large-registry retrieval or open-world tools.
