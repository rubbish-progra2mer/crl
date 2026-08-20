# Bits-over-Random, a complete walkthrough

This is a guided tour of the repository. It starts with the problem, builds the math from scratch, and then reads every module down to the individual lines. The goal is simple. By the end, you should be able to close this file and rewrite the package from memory. That is the real test of understanding.

The math section is the steepest part. The code that follows it is short.

The order is the problem first, then the math, then the four modules in the order they depend on each other, which is `metrics.py`, then `audit.py`, then `logs.py`, then `cli.py`. After that come the examples, the tests, and finally how to read an audit report like a practitioner.

---

## 1. The problem

A retrieval system is asked a simple thing. Out of N candidates, return K, and call it a success if at least one relevant item is in those K. Success@K is the fraction of queries where that happened.

Success@K has a floor, and that floor has nothing to do with how good your system is. If relevant items are common, or K is large, a blind random draw also succeeds. A system can score 99% while doing nothing at all.

The paper behind this package opens with two librarians. A library holds 1,000 books, 10 of them relevant to your query. Librarian A returns 20 books, 6 relevant, which is 30% precision and 60% recall. Librarian B returns 12 books, 4 relevant, which is 33% precision and 40% recall. Recall and F1 prefer A. But A handed over 14 irrelevant books against B's 8, and when the reader is a model that cannot skim, every irrelevant book costs attention and tokens. Compare each librarian to a blind draw of the same size and the ranking flips. B is the more selective one. And underneath A versus B sits the deeper question this package answers. Is either librarian objectively good? Not better than the other, better than the dumbest baseline there is, pure random chance. Dumbest, but also the most objective one. It needs no model, no tuning, and no opinion, only counting, and it gives the answer in a number. How many bits better than chance, where each bit means twice as good as luck.

The paper then measures the floor directly, in its 20 Newsgroups stress test. The corpus has 11,314 documents in 20 categories, and treating same-category documents as relevant gives about 572 relevant documents per query, roughly 5% of the corpus. The paper reports, for BM25:

| K   | Random draw succeeds | Success@K | BoR       |
| --- | -------------------- | --------- | --------- |
| 10  | ~40%                 | 94%       | 1.22 bits |
| 100 | ~99%                 | 100%      | 0.01 bits |

At K=10 the system is doing real work, 94% against a 40% floor, 1.22 bits of a possible 1.31. At K=100 the floor itself is about 99%, so the perfect score is not evidence of anything, and the bits confirm it. The damage is not theoretical either. In the paper's downstream test, the LLM consuming the K=100 results lost 16 accuracy points compared to K=10 while paying ten times the tokens. The success metric did not become false. It stopped carrying information.

Everything in this repository exists to make that distinction measurable. Keep these numbers in your head. They come back again and again.

---

## 2. The math, from first principles

### 2.1 The random baseline

Suppose K items are drawn uniformly at random, without replacement, from N items of which R are relevant. What is the probability of getting at least one relevant item?

When you see "at least one" in probability, train yourself to count the complement instead. It is almost always easier. The number of ways to draw K items that all miss the R relevant ones is C(N−R, K), because you are choosing all K from the N−R irrelevant items. Divide by the total number of possible draws, C(N, K), and subtract from one.

```
P(no hit)  = C(N−R, K) / C(N, K)
P_rand     = 1 − C(N−R, K) / C(N, K)
```

This is the hypergeometric "at least one" probability, and it is worth appreciating that it is exact. There is no independence assumption hiding in it and no approximation. It was earned by counting.

### 2.2 Why the code works in log space

Now try to compute C(400000, 100) directly, the binomial from `examples/case2_lottery.py`. It has hundreds of digits, 403 of them, and overflows a float immediately. The cure is to never form the factorials at all and to work with their logarithms instead. The tool for that is `lgamma`, which shows up everywhere in numerical work.

Start with what `lgamma` is. The gamma function Γ generalizes the factorial beyond whole numbers, and the only fact needed here is what it does at whole numbers.

```
Γ(n + 1) = n!
```

So `lgamma(n + 1)`, the natural log of Γ(n + 1), is exactly log(n!). The shift by one is a historical convention of the gamma function, and it is the reason every argument in the code below carries a `+ 1`. Forgetting that shift is a common bug.

Why is the log safe when the factorial is not? 400000! has about two million digits, far beyond any float. Its natural log is about 4.8 million, an ordinary number that a float holds without complaint. Logs turn astronomical products into moderate sums.

And `lgamma` computes that log directly, in one call, without forming the factorial and without looping over four hundred thousand terms the way summing log(i) would. A check on a small case, using 5! = 120.

```python
>>> import math
>>> math.lgamma(6)
4.787491742782047
>>> math.log(120)
4.787491742782046
```

The two agree to the last digit or so, which is also a preview of a theme. Floating point answers are correct to about fifteen significant digits, not to infinity, and good numerical code is written with that in mind.

Now the identity, derived slowly. A binomial coefficient is a ratio of three factorials.

```
C(n, k) = n! / (k! (n−k)!)
```

Take the log of both sides. Logs turn multiplication into addition and division into subtraction.

```
log C(n, k) = log(n!) − log(k!) − log((n−k)!)
```

Replace each log-factorial using Γ(m + 1) = m!.

```
log C(n, k) = lgamma(n+1) − lgamma(k+1) − lgamma(n−k+1)
```

In `metrics.py` the identity is one line, inside `_log_choose`.

```python
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
```

So instead of forming the huge binomials, `random_success_at_least_one` works with their logs.

```python
    log_no_hit = _log_choose(N - R, K) - _log_choose(N, K)
```

That is the log of P(no hit), a probability, so it can never be positive, and it stays a modest number no matter how astronomical the binomials would have been.

### 2.3 Why `-expm1` instead of `1 − exp`

There is one more numerical problem. The last step of the formula is `P_rand = 1 − exp(log_no_hit)`. When P_rand is tiny, `exp(log_no_hit)` is a number like 0.999999999999, and subtracting it from 1 cancels almost every significant digit. The extreme case shows it.

```python
>>> import math
>>> 1 - math.exp(-1e-17)     # exp rounds to exactly 1.0
0.0
>>> -math.expm1(-1e-17)      # expm1 keeps the precision
1e-17
```

The function `expm1(x)` computes `exp(x) − 1` without ever forming the intermediate value near 1. That is exactly how `random_success_at_least_one` finishes.

```python
    return -math.expm1(log_no_hit)
```

For ordinary inputs the two ways agree. For extreme ones, only `expm1` survives. Once you have seen this trick you will start noticing it in good numerical code everywhere.

### 2.4 Generalizing to "at least m"

Sometimes success should mean at least m relevant items in the top K, not just one. The probability is the tail of the hypergeometric distribution, a sum over the exact-x probabilities.

```
P(at least m) = Σ_{x=m..min(R,K)}  C(R, x) · C(N−R, K−x) / C(N, K)
```

Each term is computed in log space, like before, and then the terms are combined with the log-sum-exp trick. The idea is to factor out the largest term so that nothing underflows. In `random_success_at_least_m` that is two lines.

```python
    peak = max(terms)
    return math.exp(peak) * sum(math.exp(t - peak) for t in terms)
```

Section 3 walks the full function, including how `terms` is built.

A quick feel for what m does. Take N=600, R=6, K=40. Getting at least one relevant item by pure luck happens 34.0% of the time. Getting at least two by luck happens only 5.5% of the time. Raising m raises the bar that a blind draw has to clear.

### 2.5 Bits-over-Random

With the floor known, the metric itself is just a ratio.

```
enrichment = P_observed / P_random
BoR        = log2(enrichment)
```

In `metrics.py` those are two functions. `enrichment_factor` ends with

```python
    return observed / random_baseline
```

and `bits_over_random` ends with

```python
    return math.log2(ef)
```

Why take the log, and why base 2? Because it turns multiplicative advantage into an additive scale with a unit you can say out loud. Each bit is one doubling over chance. BoR of 0 means the system equals a blind draw. BoR of 3 means it is 8 times better. Negative BoR means it is worse than guessing. And differences in bits are comparable across corpora and depths, which raw percentages are not. That last property is what makes the metric travel.

### 2.6 The ceiling

Observed success cannot exceed 1.0, so BoR has a hard ceiling.

```
BoR_ceiling = log2(1 / P_rand) = −log2(P_rand)
```

In code the ceiling is a literal. `bor_ceiling` plugs a perfect observed rate into the existing function.

```python
def bor_ceiling(random_baseline: float) -> float:
    return bits_over_random(observed=1.0, random_baseline=random_baseline)
```

This may be the most useful single number in the whole framework, because it judges the question rather than the system. In the 20 Newsgroups numbers from section 1, the ceiling at K=100 is about 0.01 bits. A perfect retriever, at that depth, could demonstrate about a hundredth of a doubling over chance. The evaluation is saturated. When you see a ceiling like that, the advice is not to fix the retriever. It is to change K.

### 2.7 Lambda and the collapse zone

```
lambda = K · R / N
```

In code it is the simplest function in the package.

```python
def collapse_lambda(N: int, R: int, K: int) -> float:
    _check_counts(N, R, K)
    return K * R / N
```

This is the expected number of relevant items in a random draw of size K. You can see it by linearity of expectation, since each drawn item is relevant with probability R/N. Lambda is the density dial behind everything so far.

When R is small compared to N, the hypergeometric is well approximated by a Poisson with mean lambda, which gives a useful rule of thumb.

```
P_rand ≈ 1 − e^(−λ)
```

Try lambda equal to 3. Then 1 − e⁻³ = 0.950. As an exact check, take N=10,000, R=100, K=300, where lambda is exactly 3, and the true P_rand comes out to 0.953.

One consequence is visible in the command line tool, which prints two warnings.

```python
    if p_rand >= 0.95:
        print("warning: random baseline is already near 1.0")
    if lam >= 3:
        print("warning: lambda is in the collapse zone")
```

They are the same boundary seen from two sides, which is why, in the sparse regime where R is small compared to N, they fire together. Outside that regime the two can disagree, for example at N=100, R=1, K=96 the baseline warning fires while lambda sits at 0.96, and there the exact baseline is the one to trust. Past the boundary you are in the collapse zone. The blind draw succeeds so often that Success@K has become decorative.

That is all the math. The rest of the package is delivery.

---

## 3. `metrics.py`, the kernel, line by line

One file, no dependencies beyond `math`, pure arithmetic on five numbers. Read it function by function.

### 3.1 Validation

```python
def _check_counts(N: int, R: int, K: int) -> None:
    if N <= 0:
        raise ValueError("N must be positive.")
    if R < 0 or R > N:
        raise ValueError("R must satisfy 0 <= R <= N.")
    if K < 0 or K > N:
        raise ValueError("K must satisfy 0 <= K <= N.")
```

Three comparisons, called once at the top of every public combinatorial function. Note what is allowed. R = 0 and K = 0 are valid inputs. `_check_counts` lets them through, and each function's own guards decide what they mean, `random_success_at_least_one` returns 0.0 for them, while `random_success_at_least_m` returns 1.0 when m is 0, since at least zero successes is certain. Only true contradictions raise, like a negative count or more relevant items than items. The principle, nonsense should fail loudly at the door, but degenerate inputs that are still coherent should flow through and produce the correct degenerate answer.

### 3.2 Log binomials

```python
def _log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
```

The second line is section 2.2 written down. The first line is a design choice. An impossible binomial, like choosing 7 items from 5, returns log(0), which is negative infinity, instead of raising an error.

Why allow that? Because this function gets used inside sums of exponentials, and `exp(-inf)` is exactly 0.0. That means impossible terms vanish from sums on their own, with no special-casing at any call site. So negative infinity here is not an error code. It is the honest mathematical answer, quietly doing the right thing everywhere this function is used.

### 3.3 The at-least-one baseline

```python
def random_success_at_least_one(N: int, R: int, K: int) -> float:
    _check_counts(N, R, K)

    if K == 0 or R == 0:
        return 0.0
    if K > N - R:
        return 1.0

    log_no_hit = _log_choose(N - R, K) - _log_choose(N, K)
    return -math.expm1(log_no_hit)
```

Read the guards in order, and notice that each one is a sentence. If K is 0 or R is 0, the draw is empty or there is nothing to hit, so the probability is exactly 0. If K is greater than N − R, there are fewer irrelevant items than slots in the draw, so the draw cannot avoid the relevant items even if it tries, and the probability is exactly 1. Both of these exits happen before any floating point math, which makes the function bit-exact at its boundaries. Good code gets its edge cases exactly right rather than approximately right.

The general case is just two lines. The complement in log space, which is sections 2.1 and 2.2, then the `expm1` finish from 2.3. One note about the sign. `log_no_hit` is at most 0, so `expm1(log_no_hit)` equals P(no hit) − 1, which is at most 0, and the leading minus flips it into 1 − P(no hit).

### 3.4 The at-least-m tail

```python
def random_success_at_least_m(N: int, R: int, K: int, m: int) -> float:
    _check_counts(N, R, K)

    if m <= 0:
        return 1.0
    if m > R or m > K:
        return 0.0

    upper = min(R, K)
    terms = [
        _log_choose(R, x) + _log_choose(N - R, K - x) - _log_choose(N, K)
        for x in range(m, upper + 1)
    ]

    peak = max(terms)
    return math.exp(peak) * sum(math.exp(t - peak) for t in terms)
```

Guards first, same discipline as before. At least 0 successes is certain. At least more than exist, or more than you draw, is impossible.

The middle of the function deserves a slower pass. Start with the probability of one exact outcome. The draw contains exactly x relevant items when two choices line up. Which x of the R relevant items landed in the draw, C(R, x) ways. Which K − x of the N − R irrelevant items filled the remaining slots, C(N − R, K − x) ways. Divide by C(N, K), the number of possible draws.

```
P(exactly x) = C(R, x) · C(N − R, K − x) / C(N, K)
```

Next the range of x. It starts at m, because the function wants the probability of at least m. It ends at min(R, K), because the draw cannot contain more relevant items than exist, which is R, and cannot contain more items than it holds, which is K. That bound is the line `upper = min(R, K)`. The `+ 1` in `range(m, upper + 1)` exists because `range` excludes its endpoint, and upper must be included.

"At least m" is then the sum of the exact outcomes from m to upper. Written as a direct loop in plain probabilities, with `math.comb` for the binomials, it looks like this.

```python
# sketch, not the repo code
total = 0.0
for x in range(m, upper + 1):
    total += math.comb(R, x) * math.comb(N - R, K - x) / math.comb(N, K)
return total
```

This is correct, and for small inputs it is fine. At the sizes from section 2.2 the binomials are integers hundreds of digits long, so the repo stays in log space instead, using the same identity as before. Multiplication of terms becomes addition of logs, division becomes subtraction. The loop now collects the log of each term rather than adding probabilities, because the terms still have to be combined, and that combination is the log-sum-exp step below.

```python
# sketch, not the repo code
terms = []
for x in range(m, upper + 1):
    terms.append(_log_choose(R, x) + _log_choose(N - R, K - x) - _log_choose(N, K))
```

The repo writes that loop as a list comprehension, the same computation as a single expression.

```python
    upper = min(R, K)
    terms = [
        _log_choose(R, x) + _log_choose(N - R, K - x) - _log_choose(N, K)
        for x in range(m, upper + 1)
    ]
```

Now the last two lines, which are the log-sum-exp trick promised in section 2.4. `peak = max(terms)` finds the dominant term. After subtracting it, every `exp(t - peak)` is at most 1, so nothing overflows and the terms that matter do not underflow either. The single `exp(peak)` at the front restores the true magnitude. This is also where section 3.2 pays off. If some term was negative infinity because that particular x was impossible, then `exp(-inf - peak)` is 0.0 and it contributes nothing.

### 3.5 The recall baseline

```python
def random_recall_baseline(N: int, K: int) -> float:
    if N <= 0:
        raise ValueError("N must be positive.")
    if K < 0 or K > N:
        raise ValueError("K must satisfy 0 <= K <= N.")
    return K / N
```

The same idea applied to recall instead of success. A blind draw of K items captures, in expectation, K/N of any fixed set of items. Notice that R does not appear anywhere. The expected random recall is K/N no matter how many relevant items there are, which is why this function takes only two arguments and inlines its own validation instead of calling `_check_counts`. There is simply no R to check.

### 3.6 Enrichment and bits

```python
def enrichment_factor(observed: float, random_baseline: float) -> float:
    if observed < 0:
        raise ValueError("observed must be non-negative.")
    if random_baseline < 0:
        raise ValueError("random_baseline must be non-negative.")

    if random_baseline == 0:
        if observed == 0:
            return float("nan")
        return float("inf")

    return observed / random_baseline
```

This is the linear version of the metric, and the place where the degenerate cases get decided once and deliberately. Success of 0 against a baseline of 0 returns NaN, meaning nothing was learned in either direction. Positive success where chance had literally zero probability returns positive infinity, meaning infinitely better than chance. These are semantic choices, not accidents, and putting them in the linear function means the log version inherits them for free.

```python
def bits_over_random(observed: float, random_baseline: float) -> float:
    ef = enrichment_factor(observed, random_baseline)

    if ef == 0:
        return float("-inf")
    if math.isnan(ef) or math.isinf(ef):
        return ef

    return math.log2(ef)
```

There are three exits before the log. If the enrichment is 0, meaning nothing was observed while chance would have found something, then log2(0) would raise, so the function returns negative infinity explicitly, infinitely worse than chance. NaN and the infinities pass through unchanged, because the log of "no information" is still no information, and the log of "infinitely better" is still infinitely better. Only finite positive ratios ever reach `math.log2`. When you write functions like this yourself, handle the degenerate cases in one place and let everything downstream inherit them. It keeps the rules from drifting apart.

### 3.7 The conveniences

```python
def bor_success_at_one(observed: float, N: int, R: int, K: int) -> float:
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    return bits_over_random(observed=observed, random_baseline=p_rand)


def bor_ceiling(random_baseline: float) -> float:
    return bits_over_random(observed=1.0, random_baseline=random_baseline)


def collapse_lambda(N: int, R: int, K: int) -> float:
    _check_counts(N, R, K)
    return K * R / N
```

`bor_success_at_one` is composition and nothing more. `bor_ceiling` is section 2.6 implemented as a literal. It plugs observed = 1.0 into the existing function rather than writing `-log2(p)` separately, so there is one code path and one set of degenerate-case rules. Notice the consequence, needed later. `bor_ceiling(0.0)` returns positive infinity through the inherited rules, and section 4 will have to handle that. `collapse_lambda` is the expectation from 2.7, validated like its siblings.

You now know everything the kernel knows. Everything from here on is about getting real-world data into it and honest reports out of it.

---

## 4. `audit.py`, from one number to a log, line by line

The calculator answers one question. Given aggregate N, R, K and an observed rate, how many bits? But production retrieval is not one number. It is a log of events, each with its own pool size, depth, and outcome. The auditor is the piece that ingests that.

### 4.1 `QueryRecord`

```python
@dataclass
class QueryRecord:
    N: int
    R: int
    K: int
    hit: bool
    m: int = 1
    qid: Optional[str] = None
    scores: Optional[Sequence[float]] = None

    @property
    def p_rand(self) -> float:
        if self.m <= 1:
            return random_success_at_least_one(N=self.N, R=self.R, K=self.K)
        return random_success_at_least_m(N=self.N, R=self.R, K=self.K, m=self.m)

    @property
    def lam(self) -> float:
        return collapse_lambda(N=self.N, R=self.R, K=self.K)
```

One retrieval event. The field names are uppercase on purpose, so that `QueryRecord(N=600, R=6, K=40, ...)` reads the same as `random_success_at_least_one(N=..., R=..., K=...)`. Consistency like this is a kindness to the next reader, who is usually you in three months.

The `p_rand` property dispatches on m. The default is the at-least-one baseline, and any individual record can demand a stricter definition of success. The `scores` field is carried but not consumed yet. It is the seat reserved for the K-sweep feature, declared now so that the log format will not have to change later. And note that records are independent of each other. Nothing anywhere assumes the pool is the same across queries.

### 4.2 `audit()`, the aggregation

```python
    recs = list(records)
    if not recs:
        raise ValueError("No query records to audit.")

    p_obs = sum(1 for q in recs if q.hit) / len(recs)
    p_rand_vals = [q.p_rand for q in recs]
    p_rand_mean = sum(p_rand_vals) / len(p_rand_vals)
    lambda_mean = sum(q.lam for q in recs) / len(recs)
```

Why `list(records)` first? The parameter accepts any iterable, possibly a generator that can be consumed only once, and this function needs multiple passes, first for the aggregate and later for the bootstrap. So it materializes exactly once, up front. The empty check raises rather than returning an empty result, because an audit of nothing is a bug at the call site, not a finding.

Notice also that `p_rand_vals` is computed once and reused for three computations below, the mean, the ceilings, and the collapse-zone count. Each `q.p_rand` is a hypergeometric evaluation, so the caching is not cosmetic. The bootstrap, as section 4.3 will admit, does not yet use this cache.

Now the most important design decision in the file. BoR is computed as `log2(mean(hit) / mean(p_rand))`. Why not the mean of per-query BoR instead? Because per-query BoR does not exist. A single query's outcome is binary, and log2(0/p) is negative infinity for every miss. BoR is a population statistic. Averaging the observed successes and the baselines separately, then taking one log ratio, compares the population's hit rate to the hit rate that this same population of questions would produce under blind drawing. And it stays well defined when every query has a different N, R, and K, which in real logs they do.

```python
    ceilings = [bor_ceiling(p) for p in p_rand_vals]
    finite = [c for c in ceilings if math.isfinite(c)]
    ceiling_mean = sum(finite) / len(finite) if finite else float("inf")

    frac_zone = sum(1 for p in p_rand_vals if p >= 0.95) / len(p_rand_vals)
    bor = bits_over_random(observed=p_obs, random_baseline=p_rand_mean)
```

Remember the warning from section 3.7? Here is where it lands. A record with R = 0 has a `p_rand` of exactly 0.0, and `bor_ceiling(0.0)` is positive infinity by the inherited rules. One such row would turn the mean ceiling into infinity and ruin the report. The `isfinite` filter keeps the ceiling meaningful, and if no ceiling at all is finite, the mean is honestly infinity.

`frac_zone` counts the queries whose individual baseline is at or above 0.95. This is the per-query collapse-zone test, and it catches a case the aggregate can hide. A log can look fine on average while half its traffic is being asked saturated questions. This number is how you see that.

### 4.3 The bootstrap

```python
    rng = _random.Random(seed)
    n = len(recs)
    boot = []
    for _ in range(n_bootstrap):
        s_hits = 0
        s_pr = 0.0
        for _ in range(n):
            q = recs[rng.randrange(n)]
            s_hits += q.hit
            s_pr += q.p_rand
        boot.append(
            bits_over_random(observed=s_hits / n, random_baseline=s_pr / n)
        )
    boot.sort()
    ci = (boot[int(0.025 * n_bootstrap)], boot[min(int(0.975 * n_bootstrap), n_bootstrap - 1)])
```

Walk it line by line, because there is a small lesson in nearly every one.

`_random.Random(seed)` creates a private random generator, seeded with a default of 0. Two benefits. Audits are reproducible, and the module never touches the global random state of whatever program imported it. The module is imported under the name `_random` so it cannot collide with anything else in the file.

The inner loop draws n indices with replacement using `rng.randrange(n)`, and that is the entire bootstrap idea. Each resample is a plausible alternative log of the same size, built from the same queries.

`s_hits += q.hit` works because in Python a bool is a subtype of int, so True adds 1. Two running sums are accumulated instead of building resampled lists, which keeps the loop free of allocations. This body runs n_bootstrap · n times, which is 2000 · n with the defaults, so it is the hot path.

One honest confession about this loop. Each resample touches `q.p_rand`, which is a property and therefore recomputes the hypergeometric, even though `p_rand_vals` was cached above for the aggregate. That is the known cost of keeping `QueryRecord` a plain dataclass. If profiling ever flags it, the fix is to index into `p_rand_vals` instead of touching the record. This is written down so that when you find it yourself, you know it was a choice and not an oversight.

Finally, `boot.sort()` and the two indices implement the percentile method. With the default of 2000 resamples, the indices are 50 and 1950, the empirical 2.5th and 97.5th percentiles. The `min(..., n_bootstrap - 1)` guard never actually fires. For any positive count, `int(0.975 · n)` lands strictly below n, so the index is always in range. The guard is purely defensive, there so the line stays safe if the percentile constant is ever edited, not because the current constant needs it.

Why bootstrap at all instead of a formula? Because the statistic is a log of a ratio of two means over heterogeneous baselines. There is no clean closed form, and the bootstrap is honest, and at typical log sizes it costs seconds, not minutes.

One subtlety the tests caught. On a degenerate log where every query is a hit, every resample is logically identical to the aggregate, yet the CI endpoints differed from the point estimate by a couple of units in the last place. The cause is not ordering, both routes add the same values left to right. The aggregate mean uses the built-in `sum`, which in modern CPython, 3.12 and later, applies compensated Neumaier summation to floats, while the bootstrap accumulates with a plain `+=` loop, so the two routes round differently even over bit-identical values. Measured on the failing case, the two sums differ by about 1.6e-14, which moves the bits by two units in the last place. This is why float comparisons in the tests use tolerances. Two float sums computed by different routes should be compared with one.

### 4.4 The verdict

```python
def _verdict(bor: float, p_obs: float, p_rand: float, frac_zone: float) -> str:
    if frac_zone >= 0.5:
        return (
            f"COLLAPSE ZONE: {frac_zone:.0%} of queries have a random "
            ...
        )
    if math.isnan(bor):
        return (
            f"UNDEFINED: observed {p_obs:.0%} against a random baseline "
            ...
        )
    if math.isinf(bor) and bor > 0:
        return (
            f"SELECTIVE: observed {p_obs:.0%} where the random baseline "
            ...
        )
    if bor <= 0.0:
        return (
            f"AT/BELOW RANDOM: observed {p_obs:.0%} against a blind-draw "
            ...
        )
    if bor < 1.0:
        return (f"WEAK: {bor:.2f} bits over random. ...")
    return (f"SELECTIVE: {bor:.2f} bits over random, about {2 ** bor:.1f}x ...")
```

An if chain where the order is the design. The collapse-zone check comes first on purpose. A high observed rate inside the zone is exactly the paradox from section 1, and it must never be allowed to print as success. Even a log with BoR above 1 gets the COLLAPSE ZONE verdict if half its questions are saturated. Two guards for non-finite ratios come next, and they exist because NaN fails every comparison while positive infinity passes the final one, so without them both would fall through and print nonsense like SELECTIVE with nan bits. A NaN ratio, zero observed against a zero baseline, returns UNDEFINED. A positively infinite ratio, success against a zero baseline, returns a SELECTIVE message saying the bits are unbounded instead of printing inf. Negative infinity needs no guard, it is caught by the sign check. After that comes the sign of BoR, then the one-bit line, one full doubling over chance, which separates WEAK from SELECTIVE. The last line converts bits back into a multiplier with `2 ** bor`, because "2.4 times better than a blind draw" lands with people who do not think in logarithms, and most people do not.

So the verdicts, in the order they are checked. Half or more of the queries in the zone gives COLLAPSE ZONE. A NaN ratio gives UNDEFINED. A positively infinite ratio gives the unbounded SELECTIVE message. BoR at or below zero gives AT/BELOW RANDOM. Between zero and one gives WEAK. One or more gives SELECTIVE.

`AuditResult` itself is just a report dataclass. The fields, the CI tuple, the verdict string, plus `per_query` holding the records, which is excluded from the repr so that printing a result does not dump 800 rows into your terminal, and a `summary()` method that formats the block the CLI prints.

---

## 5. `logs.py`, reading other people's logs, line by line

The auditor is only useful if it can eat logs it has never seen. Teams already store retrieval events for their dashboards. This module reads that exhaust. It is read-only, it runs locally, and nothing leaves the machine.

### 5.1 The alias table and resolver

```python
ALIASES = {
    "N": ["N", "n", "pool_size", "corpus_size", "num_candidates",
          "total_tools", "total_docs", "total"],
    "K": ["K", "k", "depth", "top_k", "topk", "num_shown",
          "num_retrieved", "shortlist_size"],
    "hit": ["hit", "success", "found", "solved", "contains_relevant",
            "task_success", "label"],
    "R": ["R", "r", "relevant", "num_relevant", "n_relevant",
          "relevant_count"],
    "qid": ["qid", "query_id", "id", "request_id", "trace_id"],
}
```

Each list is ordered, with the canonical name first and then the names in descending likelihood. The order matters because resolution takes the first match. A row that contains both `N` and `pool_size` resolves to `N`.

```python
def _resolve(row: Mapping, key: str, mapping: Optional[Mapping[str, str]]):
    if mapping and key in mapping:
        return row.get(mapping[key])
    for alias in ALIASES[key]:
        if alias in row:
            return row[alias]
    return None
```

Two tiers of precedence in five lines. If the caller supplied an explicit mapping for this key, it wins outright. It uses `row.get`, so a mapped field that is absent yields None. The reasoning goes like this. The caller said exactly where to look, so absence there is a missing value, not an invitation to fall back to guessing. Only when there is no mapping does the alias scan run, with the `in` check before indexing so absent aliases are skipped rather than raising KeyError. None is the universal "not found" signal that the row loop downstream understands.

### 5.2 Truthiness

```python
_TRUE = {"true", "1", "yes", "y", "t", "hit", "success"}


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0
    return str(value).strip().lower() in _TRUE
```

The order of the first two checks matters, because in Python a bool is a subclass of int, so `isinstance(True, int)` is True. If the numeric check came first, booleans would take that branch. In this particular case the result would happen to be the same, since True > 0 is also True, but the explicit bool-first order makes the intent unambiguous and survives any future edit to the numeric branch. Write your dispatch order to express your intent, not to rely on a coincidence.

The third line exists because CSV values arrive as strings. Strip, lowercase, membership in a closed set. Anything outside the set, including "false", "0", and any typo, reads as False. Think about which way that fails. A mangled success flag becomes a miss, which can only make the audited system look worse, never better. When you must fail, fail in the direction that cannot flatter you.

### 5.3 The row loop

```python
def _rows_to_records(
    rows: Iterable[Mapping],
    mapping: Optional[Mapping[str, str]],
    default_R: Optional[int],
    R_frac: Optional[float],
    strict: bool,
) -> Iterator[QueryRecord]:
    for i, row in enumerate(rows):
        N = _resolve(row, "N", mapping)
        K = _resolve(row, "K", mapping)
        hit = _resolve(row, "hit", mapping)
        if N is None or K is None or hit is None:
            if strict:
                missing = [
                    name for name, v in (("N", N), ("K", K), ("hit", hit))
                    if v is None
                ]
                raise ValueError(
                    f"Row {i}: missing field(s) {missing}; "
                    f"keys present: {sorted(row.keys())}."
                )
            continue
        N, K = int(N), int(K)
        K = min(K, N)
```

The `enumerate` exists purely for the error messages. "Row 41" is something a person can act on. "A row somewhere" is not. The strict branch builds the list of missing fields, and then does the thing that saves the user a round trip. It prints `sorted(row.keys())`, the keys that were actually there, so the fix is visible inside the error itself. The user sees their field is called `n_docs` and immediately knows to pass `--map N=n_docs`. Write error messages that contain their own remedy whenever you can.

Lenient mode, the bare `continue`, is the default because real logs contain rows that are not retrieval events. Heartbeats, status lines, rows from other subsystems. An audit should not die because row 7,312 of 80,000 is a heartbeat. The leniency is narrow, though. It covers rows that parse but lack one of the three required fields. A line that is not valid JSON still raises inside `from_jsonl`, in `json.loads`, and a field that cannot be converted still raises at `int(...)`. A corrupted file fails loudly instead of being silently half-read.

Now look at `K = min(K, N)` and ask why the clamp lives in the loader and not in `QueryRecord`. This placement is a decision. The kernel in `metrics.py` raises on K > N, because a caller constructing records by hand wrote a contradiction and should be told. But a log with K > N is a recording artifact. The loader clamps it and keeps reading. Same condition, two different sins, two different treatments.

```python
        R = _resolve(row, "R", mapping)
        if R is not None:
            R = int(R)
        elif default_R is not None:
            R = default_R
        elif R_frac is not None:
            R = max(1, round(R_frac * N))
        else:
            raise ValueError(
                f"Row {i}: no relevant-count field found and no default_R "
                f"or R_frac given. Logs usually drop R; pass R_frac "
                f"(for example 0.05) as an explicit, reported estimate."
            )
        R = min(R, N)
```

This is the R precedence chain, read top to bottom. A per-row field beats `default_R`, which beats `R_frac`, which beats an error. R is the field that dashboards drop most often, because teams keep what they graph, and they graph scores and outcomes.

Two details deserve your attention. First, `max(1, round(R_frac * N))` floors the estimate at 1, because an R of 0 would make every baseline 0 and every hit "infinitely better than chance". For the estimate to be coherent, even a tiny pool must contain something to find. Second, the final `else` raises, with the fix written into the message. This is a deliberate stance and maybe the most important sentence in this document. The entire purpose of this package is honesty about baselines, so it must never invent its own inputs quietly.

```python
        qid = _resolve(row, "qid", mapping)
        yield QueryRecord(
            N=N, R=R, K=K, hit=_to_bool(hit),
            qid=str(qid) if qid is not None else None,
        )
```

Notice it is `yield`, not append. The row loop is a generator, so it composes with any row source, and a strict-mode failure raises at the offending row, carrying its row number. The public loaders below do materialize the result with `list`, so the laziness is a property of this loop, not a promise about the loaders.

### 5.4 The two file formats

```python
def from_jsonl(
    path: Union[str, Path],
    *,
    mapping: Optional[Mapping[str, str]] = None,
    default_R: Optional[int] = None,
    R_frac: Optional[float] = None,
    strict: bool = False,
) -> list:
    """Load QueryRecords from a JSONL retrieval log. Read-only and local."""
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return list(_rows_to_records(rows, mapping, default_R, R_frac, strict))
```

The strip-then-skip exists because real logs sometimes contain blank lines, and `json.loads` raises on an empty string. The strip also normalizes each line before the emptiness test, so a line of pure whitespace is skipped rather than parsed. The lone `*` in the signature makes every option keyword-only. The reason is readability at the call site. A call like `from_jsonl(path, 0.05)` would leave the reader guessing which option 0.05 is, so the API simply refuses to allow it.

```python
def from_csv(
    path: Union[str, Path],
    *,
    mapping: Optional[Mapping[str, str]] = None,
    default_R: Optional[int] = None,
    R_frac: Optional[float] = None,
    strict: bool = False,
) -> list:
    """Load QueryRecords from a CSV retrieval log. Read-only and local."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return list(_rows_to_records(rows, mapping, default_R, R_frac, strict))
```

The `newline=""` is not decoration. The csv module documents it as required so that universal newline translation does not corrupt quoted fields containing line breaks, and on Windows it is the difference between correct and subtly broken parsing. `DictReader` hands each row to the same `_rows_to_records` as the JSONL path, and the string branch of `_to_bool` from section 5.2 absorbs the fact that CSV values are all strings. The two loaders differ only in parsing. Every rule lives once, in the shared row loop, which is exactly where you want your rules to live.

---

## 6. `cli.py`, two tools, one entry point, line by line

### 6.1 The dispatch

```python
def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] == "audit":
        _audit_main(argv[1:])
        return
    _calc_main(argv)
```

Five lines, and the most constrained decision in the repository, so the full reasoning deserves to be spelled out. The requirement was to add `bor audit <log>` while keeping the original `bor --N ... --R ... --K ... --observed ...` working byte for byte. The textbook tool for subcommands is argparse subparsers, and here it fits badly. The legacy invocation has required top-level options, and mixing those with an optional subcommand turns into manual validation and fragile precedence rules either way. Dispatching by hand is simpler, and it is provably non-breaking.

So the dispatch is done by hand. Peek at the first token. If it is the literal word `audit`, hand the rest, `argv[1:]`, to the subcommand parser. Otherwise hand everything, untouched, to the original parser. The `argv and` guard covers the empty invocation, so a bare `bor` falls through to the calculator and prints its usage error exactly as it always did.

Every trick has a cost, so here is this one stated honestly. A future second subcommand has to repeat the pattern, and a file literally named `audit` could never be the first positional argument to the calculator. Since the calculator takes no positional arguments at all, that collision is impossible, which is why the trick is safe here. If the calculator ever grows a positional argument, revisit this.

### 6.2 The calculator, preserved

```python
def _calc_main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="bor",
        ...
    )
    parser.add_argument("--N", type=int, required=True, help="Corpus size.")
    ...
    args = parser.parse_args(argv)

    if args.m == 1:
        p_rand = random_success_at_least_one(args.N, args.R, args.K)
    else:
        p_rand = random_success_at_least_m(args.N, args.R, args.K, args.m)
    ...
    if p_rand >= 0.95:
        print("warning: random baseline is already near 1.0")
    if lam >= 3:
        print("warning: lambda is in the collapse zone")
```

The body is the original CLI with three mechanical changes. First, `prog="bor"`, so the usage text stays correct now that the function has a private name. Second, `parse_args(argv)` instead of the implicit `sys.argv`, so the dispatch controls what the parser sees. Third, the description text now mentions the audit subcommand. The printed output is unchanged. The `--m` switch picks between the two baselines from section 3. And the two warning thresholds are the boundary from section 2.7, seen from both sides. As derived there, in the sparse regime they fire together by construction, not by coincidence. It is a nice feeling when a line of theory explains a line of output.

### 6.3 The audit subcommand

```python
    mapping = None
    if args.map:
        mapping = dict(pair.split("=", 1) for pair in args.map.split(","))
```

The string from `--map N=pool_size,K=top_k` becomes a dict in one line. Each pair reads canonical key on the left, log field name on the right. The detail that matters is the `1` in `split("=", 1)`. Only the first equals sign separates key from value, so the field name on the right may itself contain equals signs. A log column literally named `score=raw` exists somewhere in the world, and `--map hit=score=raw` parses into the pair `("hit", "score=raw")` and loads correctly. Without the maxsplit, that pair would split into three pieces and the dict construction would raise.

```python
    loader = from_csv if args.csv else from_jsonl
    try:
        records = loader(
            args.log,
            mapping=mapping,
            default_R=args.default_R,
            R_frac=args.R_frac,
            strict=args.strict,
        )
    except FileNotFoundError:
        parser.error(f"log file not found: {args.log}")
    except ValueError as e:
        parser.error(str(e))
```

The loader ternary works only because the two loaders share a signature, which was a design choice back in section 5.4 paying off here. The try and except blocks are the CLI's manners. `parser.error` prints a one-line message plus the usage text and exits with code 2, which is the argparse convention for usage errors. A wrong path, or a log with no R and no `--R-frac`, should never print a nine-frame traceback at someone who just wants to know whether their retriever works. And notice that the ValueError branch reuses the loader's own message, the one from section 5.3 that names the row and contains its own fix. Friendliness composes when you build it in at every layer.

```python
    result = audit(records, n_bootstrap=args.bootstrap, seed=args.seed)
    print(result.summary())
    if args.R_frac is not None:
        print(
            f"note: R estimated as round({args.R_frac} * N) per row; "
            f"treat BoR as an estimate."
        )
```

The closing conditional prints the estimate note whenever `--R-frac` was passed. The note keys on the flag, not on actual use, so it prints even when every row carried its own R and the estimate never fired. `--default-R` is also an estimate and currently gets no note. Tightening both would require the loader to report whether a fallback actually fired, a reasonable future change.

---

## 7. The examples as case studies

**`case2_lottery.py`** shows the paradox in four lines per row.

```python
for K, observed in [(10, 0.82), (100, 1.00)]:
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    bor = bor_success_at_one(observed=observed, N=N, R=R, K=K)
    lam = collapse_lambda(N=N, R=R, K=K)
```

The same hypothetical system at K=10, where observed 0.82 over a 0.401 floor gives 1.03 bits, which is real, and at K=100, where observed 1.00 over a 0.994 floor gives 0.009 bits, which is nothing. Coverage went up while information went to zero. If you only ever run one example, run this one.

**`tool_selection_58.py`** shows the ceiling as a design tool.

```python
for K in [5, 20, 58]:
    p_rand = random_success_at_least_one(N=N, R=R, K=K)
    ceiling = bor_ceiling(p_rand)
    lam = collapse_lambda(N=N, R=R, K=K)
```

A 58 tool registry with 4 relevant tools per task. Show 5 tools and a perfect selector can demonstrate 1.69 bits. Show 20 and the ceiling is 0.28 bits. Show all 58 and it is exactly 0. Before you tune a tool shortlist, this tells you which depths are even worth evaluating at.

**`audit_logs_demo.py`** runs the full loop. It writes a synthetic JSONL log in someone else's field names, `pool_size`, `top_k`, `found`, then loads and audits it with zero configuration.

```python
records = from_jsonl(LOG)
print(audit(records).summary())
```

Those two lines are the whole integration, and the script ends by printing the next command to run. The simulated retriever multiplies each row's blind-draw rate by 2.5 and caps the result at probability 1.0, and the cap matters, with the demo's seed about a quarter of the rows, 194 of 800, saturate. The population's true enrichment is therefore not log2 of 2.5, which is 1.32 bits, but the capped expectation, which works out to about 2.41 times chance, 1.27 bits. The audit recovers +1.28 with a confidence interval that covers the capped truth. The auditor recovering a computable ground truth is the best sanity check available.

---

## 8. The tests, and what each one pins down

The original `tests/test_metrics.py` pins the kernel arithmetic.

`tests/test_audit.py` pins six things. The `case2_lottery.py` parameters, 400,000 documents with 20,000 relevant at K=100, land in the COLLAPSE ZONE verdict with BoR near 0. A perfect retriever's BoR equals the ceiling identity, which is minus log2 of P_rand, and sits inside its own confidence interval, with the float-tolerance lesson from section 4.3 baked in. The operative lines of that second test:

```python
    assert math.isclose(result.bor, -math.log2(p_rand), rel_tol=1e-9)
    lo, hi = result.bor_ci
    eps = 1e-9
    assert lo - eps <= result.bor <= hi + eps
```

A below-random log gets the AT/BELOW RANDOM verdict. An empty log raises. And the two non-finite cases are pinned, a zero baseline with zero observed yields the UNDEFINED verdict, and a zero baseline with any success yields the unbounded SELECTIVE message.

`tests/test_logs.py` pins the loader. Alias resolution on realistic field names. The explicit mapping override. `R_frac` estimation and the full R precedence chain, per-row R beats `default_R`, and `default_R` beats `R_frac`. The actionable error when R is unavailable. Lenient skip versus strict raise on rows missing required fields. And the CSV path end to end.

Together they freeze the two contracts that matter. The math is the paper's math, and the loader never silently invents data.

---

## 9. How to read an audit

Here is the demo's output, annotated the way it would be talked through on a whiteboard.

```
queries analyzed          : 800        <- sample size; CIs shrink with it
observed success (P_obs)  : 0.8113     <- what the dashboard graphs
random baseline (P_rand)  : 0.3351     <- what a blind draw would graph
Bits-over-Random          : +1.2758    <- the part that is actually skill
  [95% CI +1.2297, +1.3199]            <- sampling uncertainty over queries
BoR ceiling (mean)        : 1.6481     <- best possible at these N, R, K
lambda (mean)             : 0.4015     <- density; 3+ is the collapse zone
collapse-zone queries     : 0%         <- share of saturated questions
SELECTIVE: 1.28 bits over random, about 2.4x better than a blind draw
```

The two numbers to read together are BoR and the ceiling. Here the system shows 1.28 of an available 1.65 bits, so most of the demonstrable selectivity is being realized. Hold on to this rule of thumb. A system showing 0.05 bits under a 0.05 bit ceiling is not a bad system. It is a bad question. A system showing 0.05 bits under a 2 bit ceiling is a bad system. The ceiling tells you which conversation to have.

---

## 10. What BoR does not tell you

This document closes with honesty about the tool itself, because a metric that hides its own limits is the very thing this package was built against.

R is often an estimate. When you use `--R-frac`, BoR inherits the estimate's error. Treat such audits as comparative, asking whether a change helped, more than as absolute truth.

The hit signal is whatever your log says it is. If "found" really means "the task eventually succeeded", that is execution feedback, which is useful but noisier than labeled relevance. BoR corrects for chance. It cannot correct for a mislabeled outcome.

BoR measures selection, not answer quality. It tells you whether the right thing reached the candidate set. It says nothing about what the consumer, human or model, did with it afterward.

The baseline is a uniform blind draw. That is the right floor for the question "is this retriever doing anything", and it is deliberately the lowest bar there is. Beating it is necessary, not sufficient.

The collapse zone is the one finding that needs no caveats. When the blind draw succeeds 99% of the time, a 99% success rate is not a result. That is the paradox from section 1, and now you can compute it.

Go run the examples, break something on purpose, and read the error messages. They were written for you.
