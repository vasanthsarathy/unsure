from unsure import __version__
from unsure.boe import BOE


def test_version():
    assert __version__ == "0.1.0"


THRESHOLD = 0.1


def test_combination_example1():
    """
    Example 1
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.6)
    boe1.set_mass(["b"], 0.3)
    boe1.set_mass(["a", "b"], 0.1)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.5)
    boe2.set_mass(["b"], 0.2)
    boe2.set_mass(["a", "b"], 0.3)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0.53) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0.17) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["a", "b"]) - 0.03) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.27) < THRESHOLD


def test_combination_example2():
    """
    Example 2
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.2)
    boe1.set_mass(["b"], 0.8)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.9)
    boe2.set_mass(["b"], 0.1)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0.18) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0.08) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["a", "b"]) - 0) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.74) < THRESHOLD

    # DCR
    assert abs(boe1.dcr(boe2, ["a"]) - 0.69) < THRESHOLD
    assert abs(boe1.dcr(boe2, ["b"]) - 0.3) < THRESHOLD


def test_zadeh():
    """
    Example 3 (Zadeh example)
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b", "c"])
    boe1.set_mass(["a"], 0.9)
    boe1.set_mass(["c"], 0.1)

    boe2 = BOE(["a", "b", "c"])
    boe2.set_mass(["b"], 0.9)
    boe2.set_mass(["c"], 0.1)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["c"]) - 0.01) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.99) < THRESHOLD

    # DCR
    assert abs(boe1.dcr(boe2, ["c"]) - 1) < THRESHOLD


def test_combination_example4():
    """
    Example 4 (with total conflict)
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b", "c", "d"])
    boe1.set_mass(["a"], 0.3)
    boe1.set_mass(["c"], 0.7)

    boe2 = BOE(["a", "b", "c", "d"])
    boe2.set_mass(["b"], 0.4)
    boe2.set_mass(["d"], 0.6)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["c"]) - 0) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["d"]) - 0) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 1) < THRESHOLD

    # DCR
    assert boe1.dcr(boe2, ["c"]) == None


def test_combination_example5():
    """
    Example 5
    Convergence to Idempotence
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.7)
    boe1.set_mass(["b"], 0.3)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.7)
    boe2.set_mass(["b"], 0.3)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0.49) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0.09) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.42) < THRESHOLD

    # DCR
    assert abs(boe1.dcr(boe2, ["a"]) - 0.84) < THRESHOLD
    assert abs(boe1.dcr(boe2, ["b"]) - 0.15) < THRESHOLD


def test_combination_example6():
    """
    Example 6
    Majority opinion
    Smarandache, F., & Dezert, J. (2004). A Simple Proportional Conflict Redistribution Rule.
    ArXiv:Cs/0408010. http://arxiv.org/abs/cs/0408010

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.8)
    boe1.set_mass(["b"], 0.2)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.3)
    boe2.set_mass(["b"], 0.7)

    # CONJUNCTIVE FORM
    assert abs(boe1.conjunctive_form(boe2, ["a"]) - 0.24) < THRESHOLD
    assert abs(boe1.conjunctive_form(boe2, ["b"]) - 0.14) < THRESHOLD

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.62) < THRESHOLD


def test_combination_example7():
    """
    Example 1, section 7.3
    Smarandache, F., & Dezert, J. (2005).
    Information fusion based on new proportional conflict redistribution rules.
    2005 7th International Conference on Information Fusion, 8 pp.
    https://doi.org/10.1109/ICIF.2005.1591955

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.6)
    boe1.set_mass(["a", "b"], 0.4)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["b"], 0.3)
    boe2.set_mass(["a", "b"], 0.7)

    print(boe1.pcr5(boe2, ["a", "b"]))

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.18) < THRESHOLD

    # PCR5
    assert abs(boe1.pcr5(boe2, ["a"]) - 0.54) < THRESHOLD
    assert abs(boe1.pcr5(boe2, ["b"]) - 0.18) < THRESHOLD
    assert abs(boe1.pcr5(boe2, ["a", "b"]) - 0.28) < THRESHOLD


def test_combination_example8():
    """
    Example 2, section 7.3
    Smarandache, F., & Dezert, J. (2005).
    Information fusion based on new proportional conflict redistribution rules.
    2005 7th International Conference on Information Fusion, 8 pp.
    https://doi.org/10.1109/ICIF.2005.1591955

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.6)
    boe1.set_mass(["a", "b"], 0.4)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.2)
    boe2.set_mass(["b"], 0.3)
    boe2.set_mass(["a", "b"], 0.5)

    print(boe1.pcr5(boe2, ["a", "b"]))

    # CONFLICT
    assert abs(boe1.conflict(boe2) - 0.18) < THRESHOLD

    # PCR5
    assert abs(boe1.pcr5(boe2, ["a"]) - 0.62) < THRESHOLD
    assert abs(boe1.pcr5(boe2, ["b"]) - 0.18) < THRESHOLD
    assert abs(boe1.pcr5(boe2, ["a", "b"]) - 0.2) < THRESHOLD


def test_combination_multisources_elaborate():
    """
    This test case lays out the sequence of combinations for 3 sources

    Example from Section 11.4
    "Fusion based on PCR5-approximate"

    Smarandache, F., & Dezert, J. (2005).
    Proportional Conflict Redistribution Rules for Information Fusion.
    ArXiv:Cs/0408064. http://arxiv.org/abs/cs/0408064

    """

    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.6)
    boe1.set_mass(["b"], 0.3)
    boe1.set_mass(["a", "b"], 0.1)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.2)
    boe2.set_mass(["b"], 0.3)
    boe2.set_mass(["a", "b"], 0.5)

    boe3 = BOE(["a", "b"])
    boe3.set_mass(["a"], 0.4)
    boe3.set_mass(["b"], 0.4)
    boe3.set_mass(["a", "b"], 0.2)

    boe12 = BOE(["a", "b"])
    boe12.set_mass(["a"], boe1.pcr5(boe2, ["a"]))
    boe12.set_mass(["b"], boe1.pcr5(boe2, ["b"]))
    boe12.set_mass(["a", "b"], boe1.pcr5(boe2, ["a", "b"]))

    boe123 = BOE(["a", "b"])
    boe123.set_mass(["a"], boe12.pcr5(boe3, ["a"]))
    boe123.set_mass(["b"], boe12.pcr5(boe3, ["b"]))
    boe123.set_mass(["a", "b"], boe12.pcr5(boe3, ["a", "b"]))

    assert abs(boe123.get_mass(["a"]) - 0.5) < THRESHOLD
    assert abs(boe123.get_mass(["b"]) - 0.4) < THRESHOLD
    assert abs(boe123.get_mass(["a", "b"]) - 0.01) < THRESHOLD


def test_combination_multisources():
    """
    This test unlike the above [test_combination_multisources_elaborate()]
    uses the pcr5_multisources function

    The results should be the same as above
    """
    boe1 = BOE(["a", "b"])
    boe1.set_mass(["a"], 0.6)
    boe1.set_mass(["b"], 0.3)
    boe1.set_mass(["a", "b"], 0.1)

    boe2 = BOE(["a", "b"])
    boe2.set_mass(["a"], 0.2)
    boe2.set_mass(["b"], 0.3)
    boe2.set_mass(["a", "b"], 0.5)

    boe3 = BOE(["a", "b"])
    boe3.set_mass(["a"], 0.4)
    boe3.set_mass(["b"], 0.4)
    boe3.set_mass(["a", "b"], 0.2)

    list_boes = [boe2, boe3]

    boe123 = boe1.pcr5_multisource(list_boes)

    assert abs(boe123.get_mass(["a"]) - 0.5) < THRESHOLD
    assert abs(boe123.get_mass(["b"]) - 0.4) < THRESHOLD
    assert abs(boe123.get_mass(["a", "b"]) - 0.01) < THRESHOLD
