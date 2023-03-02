# 🎲 UNSURE

UNSURE is a python package that implements Dempster-Shafer theory of uncertainty, which is an uncertainty modeling framework that is a generalization of Bayesian Approaches. 

## Install (from PyPI)

```
pip install unsure
```

## Usage

```
from unsure import BOE

boe1 = BOE(["a", "b"])
boe1.set_mass(["a"], 0.6)
boe1.set_mass(["b"], 0.3)
boe1.set_mass(["a", "b"], 0.1)
```

The `BOE` class represents a DS-theoretic body of evidence. Once instantiated as above, we can 

### enerate uncertainty intervals: 

```
boe.uncertainty(["a"])
```

### Fuse with other BOEs:

```
boe1 = BOE(["a", "b"])
boe1.set_mass(["a"], 0.6)
boe1.set_mass(["a", "b"], 0.4)

boe2 = BOE(["a", "b"])
boe2.set_mass(["b"], 0.3)
boe2.set_mass(["a", "b"], 0.7)

print(boe1.pcr5(boe2, ["a", "b"]))
```

Many other fusion operators have been implemented. See `tests\` for examples.  


### Update a BOE as new evidence is received

```
alpha = 0.5

boe = BOE(["a", "b"])
boe.set_mass_theta(1.0)

s1 = BOE(["a", "b"])
s1.set_mass(["a"], 1)

s2 = BOE(["a", "b"])
s2.set_mass(["a"], 1)

s3 = BOE(["a", "b"])
s3.set_mass(["b"], 1)

stream = [s1, s2, s3]
boe.update_stream(stream, alpha)
```

## DS-Theoretic Terminology
- theta: Frame of Discernment (FoD) (list of singletons)
- mass: a function mapping a subset of the FoD (i.e. a proposition) with number in R
    (a.k.a: basic probability assignment, mass function)
- core: F, those propositions that have mass > 0
- focal_elements: Items in F.
- belief: total support for a proposition without any ambiguity (sum of masses of subsets)
- plausibility: Extent to which a proposition is plausible (sum of masses of overlapping sets)
