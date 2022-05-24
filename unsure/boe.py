# UPDATED DS
#  v0.2
# pylint: disable=no-member
# pylint: disable=eval-used
# singleton: string
# proposition: list of strings

"""
DS-Theoretic Terminology:

theta: Frame of Discernment (FoD) (list of singletons)
mass: a function mapping a subset of the FoD (i.e. a proposition) with number in R
    (a.k.a: basic probability assignment, mass function)
core: F, those propositions that have mass > 0
focal_elements: Items in F.
belief: total support for a proposition without any ambiguity (sum of masses of subsets)
plausibility: Extent to which a proposition is plausible (sum of masses of overlapping sets)
"""

from collections import defaultdict
import copy
from itertools import chain, combinations


class BOE:
    """
    A class to represent a DS-Theoretic Body of Evidence
    """

    def __init__(self, singletons):
        """
        Constructor
        """
        # List of lowercased singletons of size n. The index of these singletons is important.
        self._frame = [x.lower() for x in singletons]

        # dict containing masses
        # this is also the masses DSVector
        # initialized to zero
        # UNNORMALIZED
        self._dsvector = defaultdict(self._default_mass)

        # Lookup table containing keys of singletons in the masses_dsvector
        self._power = self._initialize_power()

    @staticmethod
    def _default_mass():
        """
        Returns 0 for default mass
        """
        return 0

    # -------------------------------------
    # DS-Theoretic Properties

    @property
    def frame(self):
        """
        Get singletons or FoD or frame
        List of lowercased singletons of size n.
        """
        return self._frame

    @property
    def power(self):
        """
        Get power:
        Lookup table containing keys of singletons in the masses_dsvector
        """
        return self._power

    @property
    def dsvector(self):
        """
        Get the DSVector
        Dictionary of all subsets of the frame with masses

        Actually, only contains non-zero masses

        It is UNNORMALIZED, which means masses DO NOT add up to 1
        """
        return self._dsvector

    @dsvector.setter
    def dsvector(self, value):
        """
        Set the DSVector
        """
        index, mass = value
        self._dsvector.update({index: mass})

    @property
    def normalizing_constant(self):
        """
        Returns the sum of masses in the DS-Vector.
        The Masses DSVector is unnormalized and so will
        need to be divided by this normalizing constant.
        """
        return sum(self.dsvector.values())

    # ----------------------------------
    # Key DS-Theoretic Operations

    def set_mass(self, proposition, mass):
        """
        Sets mass for a proposition or a singletona

        Just updates the mass in the DSVector.
        Does NOT normalize anything
        """
        proposition = [x.lower() for x in proposition]
        index = self._get_index_from_dsvector(proposition)
        self.dsvector = (index, mass)

    def set_masses(self, dsvector_as_dict):
        """
        Sets masses for several propositions
        from a json entry
        """
        for key, value in dsvector_as_dict.items():
            self.set_mass(eval(key), value)

    def set_mass_theta(self, mass):
        """
        Sets mass for the frame
        """
        index = self._get_index_from_dsvector(self.frame)
        self.dsvector = (index, mass)

    def get_mass(self, proposition):
        """
        Get UNNORMALIZED mass for a proposition or a singleton
        """
        proposition = [x.lower() for x in proposition]
        index = self._get_index_from_dsvector(proposition)
        return self.dsvector[index]

    def get_normalized_mass(self, proposition):
        """
        Get normalized mass for a proposition
        """
        proposition = [x.lower() for x in proposition]
        return self.get_mass(proposition) / self.normalizing_constant

    def get_masses(self):
        """
        Returns a dict containing proposition and the masses for each
        """
        masses = {}
        for key, value in self.dsvector.items():
            prop = self.get_prop_from_dsvector(key)
            entry = {str(prop): value}
            masses.update(entry)
        return masses

    def get_normalized_masses(self):
        """
        Returns a dict containing proposition and the NORMALIZED masses for each
        """
        masses = self.get_masses()
        normalized_masses = {}
        for key, value in masses.items():
            nmass = value / self.normalizing_constant
            normalized_masses.update({key: nmass})
        return normalized_masses

    def get_normalized_dsvector(self):
        """
        Returns a dsvector with all the masses normalized
        """
        normalized_dsvector = {}
        for key, value in self.dsvector.items():
            if self.normalizing_constant != 0:
                normalized_mass = value / self.normalizing_constant
            else:
                normalized_mass = value
            normalized_dsvector.update({key: normalized_mass})
        return normalized_dsvector

    def get_core(self):
        """
        Returns the core (As a list of propositions)

        All subsets of the frame that have non-zero mass
        """
        core = []
        indexes = self.get_normalized_dsvector().keys()
        for number in indexes:
            core.append(self.get_prop_from_dsvector(number))
        return core

    def belief(self, proposition):
        """
        Returns belief of a proposition

        Adds masses of subset and then divides by normalizing const.

        """
        proposition = [x.lower() for x in proposition]
        non_zero_subsets = self._get_subsets_from_dsvector(proposition)
        belief = 0
        for subset in non_zero_subsets:
            mass = self.get_mass(subset)
            belief += mass
        return belief / self.normalizing_constant

    def plausibility(self, proposition):
        """
        Returns plausibility of a proposition

        Adds masses of overlapping sets and divides by normalizing const
        """
        proposition = [x.lower() for x in proposition]
        non_zero_overlaps = self._get_intersections_from_dsvector(proposition)
        plausibility = 0
        for overlapping in non_zero_overlaps:
            mass = self.get_mass(overlapping)
            plausibility += mass
        return plausibility / self.normalizing_constant

    def uncertainty(self, proposition):
        """
        Returns the uncertainty interval

        [belief, plausibility]
        """
        proposition = [x.lower() for x in proposition]
        return [self.belief(proposition), self.plausibility(proposition)]

    def get_uncertainties(self):
        """
        Returns uncertainty intervals for all items in core
        """
        uncertainties = {}
        for proposition in self.get_core():
            uncertainty = self.uncertainty(proposition)
            uncertainties.update({str(proposition): uncertainty})
        return uncertainties

    def conditional_mass(self, proposition_b, proposition_a):
        """
        Returns conditional mass (b given a)

        m(proposition_b | proposition_a)

        Works on normalized masses

        """
        proposition_a = [x.lower() for x in proposition_a]
        proposition_b = [x.lower() for x in proposition_b]
        mass_b = self.get_mass(proposition_b)
        pl_a_minus_b = 0.0
        if not mass_b == 0:
            temp = copy.copy(proposition_a)
            if temp:
                pl_a_minus_b = self.plausibility(temp)

            mass_b_given_a = mass_b / (mass_b + pl_a_minus_b)
            return mass_b_given_a
        return 0.0

    def update(self, new_frame, alpha):
        """
        CUE Algorithm
        Mass-based conditional update

        alpha: amount of weight on existing knowledge
        """

        for prop_idx_b, _mass_b in new_frame.get_normalized_dsvector().items():

            # conditional in new_frame on prop_idx_a
            total = 0
            for prop_idx_a, mass_a in new_frame.get_normalized_dsvector().items():

                prop_a = new_frame.get_prop_from_dsvector(prop_idx_a)
                prop_b = new_frame.get_prop_from_dsvector(prop_idx_b)

                mass_b_given_a = 0.0
                if set(prop_a).issubset(set(prop_b)):
                    mass_b_given_a = new_frame.conditional_mass(prop_b, prop_a)

                beta = mass_a
                mult = mass_b_given_a * beta
                total += mult

            prop_b = self.get_prop_from_dsvector(prop_idx_b)
            current_mass = self.get_normalized_mass(prop_b)
            term1 = 0.0
            if not current_mass == 0:
                term1 = alpha * current_mass
            term2 = (1 - alpha) * total
            self.set_mass(prop_b, term1 + term2)

    def update_stream(self, list_boes, alpha):
        """
        CUE update for a list of boes
        """
        print(f"Unc: {self.get_uncertainties()}")
        for idx, boe in enumerate(list_boes):
            self.update(boe, alpha)
            print(f"Unc at [{idx}]: {self.get_uncertainties()}")

    # ------------- SPECIALIZED DS HELPERS -------------------------

    def _initialize_power(self):
        """
        Initializes lookup table called "power".
        Each index i in this lookup table contains the value 2^i.
        The lookup table is of size = number of singletons,
        and represents the position of the singleton masses in massesDSVector
        """
        power = []
        for i in range(len(self.frame)):
            j = 2**i
            power.append(j)
        return power

    def _get_index_from_dsvector(self, proposition):
        """
        Returns a DSVector key of a proposition.
        Useful for various operations including setMass, etc.
        Algorithm obtained from Polpitiya paper 2017.
        """
        proposition = [x.lower() for x in proposition]
        key = 0
        for singleton in proposition:
            try:
                idx = self.frame.index(singleton)
                key += self.power[idx]
            except:
                raise ValueError(
                    "One of the singletons in the"
                    + "proposition is not found in the frame"
                )
        return key

    def get_prop_from_dsvector(self, index):
        """
        Returns a proposition given a DSVector index
        """
        indexes = self._find_powers_of_2(index)
        singletons = [self.frame[i] for i in indexes]
        return singletons

    def _get_subsets_from_dsvector(self, proposition):
        """
        Returns all the subsets of a proposition that have
        non-zero masses

        Note: This does NOT return all subsets, just those
        with non-zero mass in the dsvector
        """
        subsets = []
        for key, _value in self.dsvector.items():
            key_proposition = self.get_prop_from_dsvector(key)
            if set(key_proposition).issubset(set(proposition)):
                subsets.append(key_proposition)
        return subsets

    def _get_intersections_from_dsvector(self, proposition):
        """
        Returns all non-zero intersections
        """
        overlapping = []
        for key, _value in self.dsvector.items():
            key_proposition = self.get_prop_from_dsvector(key)
            if set(key_proposition).intersection(set(proposition)):
                overlapping.append(key_proposition)
        return overlapping

    # -------------------- COMBINATION -------------------------

    def conjunctive_form(self, another_boe, proposition):
        """
        m(self inntersection other_boe)
        """
        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        mass = 0.0
        for index1, mass1 in self.get_normalized_dsvector().items():
            for index2, mass2 in another_boe.get_normalized_dsvector().items():
                prop1 = self.get_prop_from_dsvector(index1)
                prop2 = another_boe.get_prop_from_dsvector(index2)
                if list(set(prop1) & set(prop2)) == proposition:
                    mass += mass1 * mass2
        return mass

    def disjunctive_form(self, another_boe, proposition):
        """
        m(self union other_boe)
        """
        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        mass = 0.0
        for index1, mass1 in self.get_normalized_dsvector().items():
            for index2, mass2 in another_boe.get_normalized_dsvector().items():
                prop1 = self.get_prop_from_dsvector(index1)
                prop2 = another_boe.get_prop_from_dsvector(index2)
                if list(set(prop1) | set(prop2)) == proposition:
                    mass += mass1 * mass2
        return mass

    def conflict(self, another_boe):
        """
        K (or conflict) for Combination rules
        """
        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        conflict = self.conjunctive_form(another_boe, [])
        if conflict == 1:
            return 1

        return conflict

    def dcr(self, another_boe, proposition):
        """
        Dempster's rule of combination
        """
        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        if proposition == []:
            return 0

        if self.conflict(another_boe) == 1:
            return None

        return self.conjunctive_form(another_boe, proposition) / (
            1 - self.conflict(another_boe)
        )

    def yager(self, another_boe, proposition):
        """
        Yager Combination rule
        """
        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        if proposition == []:
            return 0

        if proposition == another_boe.frame:
            return self.conjunctive_form(another_boe, proposition) + self.conflict(
                another_boe
            )

        return self.conjunctive_form(another_boe, proposition)

    def dubois_prade(self, another_boe, proposition):
        """
        Dubois and Prade

        Dubois and Prade proposed to distribute conflict among propositions that actually
        contribute to the conflict.

        """
        if proposition == []:
            return 0

        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        term1 = self.conjunctive_form(another_boe, proposition)

        term2 = 0.0
        for index1, mass1 in self.get_normalized_dsvector().items():
            for index2, mass2 in another_boe.get_normalized_dsvector().items():
                prop1 = self.get_prop_from_dsvector(index1)
                prop2 = another_boe.get_prop_from_dsvector(index2)
                if list(set(prop1) | set(prop2)) == proposition:
                    if list(set(prop1) & set(prop2)) == []:
                        term2 += mass1 * mass2

        return term1 + term2

    def pcr5(self, another_boe, proposition):
        """
        Partial Conflict Redistribution (PCR5)

        Smarandache and Dezert

        distribute the partial conflicts among the focal elements
        involved in the conflict.
        """
        proposition = [x.lower() for x in proposition]

        if proposition == []:
            return 0

        if self.frame != another_boe.frame:
            print("Cannot handle non-identical BOEs")
            return None

        term1 = self.conjunctive_form(another_boe, proposition)

        term2 = 0.0
        powers = self._powerset(self.frame)

        for item in powers:
            if list(set(proposition) & set(item)) == []:
                term2 += self.gamma(another_boe, proposition, item)

        return term1 + term2

    def gamma(self, another_boe, proposition1, proposition2):
        """
        Gamma(B,C) useful for PCR
        """

        term1_numerator = (
            self.get_normalized_mass(proposition1) ** 2
        ) * another_boe.get_normalized_mass(proposition2)

        denominator1 = self.get_normalized_mass(
            proposition1
        ) + another_boe.get_normalized_mass(proposition2)

        term2_numerator = (
            another_boe.get_normalized_mass(proposition1) ** 2
        ) * self.get_normalized_mass(proposition2)

        denominator2 = another_boe.get_normalized_mass(
            proposition1
        ) + self.get_normalized_mass(proposition2)

        ratio1 = 0
        if denominator1 != 0:
            ratio1 = term1_numerator / denominator1

        ratio2 = 0
        if denominator2 != 0:
            ratio2 = term2_numerator / denominator2

        return ratio1 + ratio2

    def pcr5_multisource(self, list_boes):
        """
        Returns a fused BOE by repeatedly calling pcr5()

        Wickramaratne reports that PCR5 is NOT
        - associative
        - idempotent
        - cannot handle non-exhaustive FoDs.
        """
        powers = list(self._powerset(self.frame))

        boe1 = copy.copy(self)
        # Doing PCR in pairs
        for _idx, boe2 in enumerate(list_boes):
            new_boe = BOE(self.frame)
            for proposition in powers:
                new_boe.set_mass(proposition, boe1.pcr5(boe2, proposition))
            boe1 = new_boe
        return boe1

    def yager_multisource(self, list_boes):
        """
        Returns a fused BOE by repeatedly calling yager()

        """
        powers = list(self._powerset(self.frame))

        boe1 = copy.copy(self)
        # Doing YAGER in pairs
        for _idx, boe2 in enumerate(list_boes):
            new_boe = BOE(self.frame)
            for proposition in powers:
                new_boe.set_mass(proposition, boe1.yager(boe2, proposition))
            boe1 = new_boe
        return boe1

    def dcr_multisource(self, list_boes):
        """
        Returns a fused BOE by repeatedly calling dcr()

        """
        powers = list(self._powerset(self.frame))

        boe1 = copy.copy(self)
        # Doing DCR in pairs
        for _idx, boe2 in enumerate(list_boes):
            new_boe = BOE(self.frame)
            for proposition in powers:
                new_boe.set_mass(proposition, boe1.dcr(boe2, proposition))
            boe1 = new_boe
        return boe1

    def dubois_prade_multisource(self, list_boes):
        """
        Returns a fused BOE by repeatedly calling dubois_prade()

        """
        powers = list(self._powerset(self.frame))

        boe1 = copy.copy(self)
        # Doing Dubois in pairs
        for _idx, boe2 in enumerate(list_boes):
            new_boe = BOE(self.frame)
            for proposition in powers:
                new_boe.set_mass(proposition, boe1.dubois_prade(boe2, proposition))
            boe1 = new_boe
        return boe1





    # ------------- GENERIC HELPERS -------------------------

    @staticmethod
    def _find_powers_of_2(number):
        """
        Returns a list of numbers which when raised to the power of 2
        and added finally, gives the integer number
        """
        indexes = []
        bits = []
        while number > 0:
            bits.append(int(number % 2))
            number = int(number / 2)

        for i, _ in enumerate(bits):
            if bits[i] == 1:
                indexes.append(i)
        return indexes

    @staticmethod
    def _powerset(iterable):
        """
        HELPER Function
        Returns power set of an iterable.

        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        """

        iterable_list = list(iterable)
        return chain.from_iterable(
            combinations(iterable_list, r) for r in range(len(iterable_list) + 1)
        )
