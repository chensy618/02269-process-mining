class PetriNet():

    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.edges = {}
        self.markings = {}

    def add_place(self, name):
        self.places[name] = 0

    def add_transition(self, name, id):
        self.transitions[name] = id

    def add_edge(self, source, target):
        # self.edges[source] = target
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append(target)
        return self 

    def get_tokens(self, place):
        return self.markings.get(place,0)

    def is_enabled(self, transition):
        # A tranistion t is enabled in a state s if all input places of t have at least one token
        input_places = [place for place, targets in self.edges.items() if transition in targets]
        for place in input_places:
            if self.get_tokens(place) < 1:
                return False
        return True
        
    def add_marking(self, place):
        self.markings[place] = self.markings.get(place, 0) + 1

    def fire_transition(self, transition):
        # firing an enabled transition removes one token from each input place and adds one token to each output place
        if self.is_enabled(transition):
            input_places = [place for place, targets in self.edges.items() if transition in targets]
            output_places = self.edges.get(transition, [])
            for place in input_places:
                self.markings[place] -= 1
            for place in output_places:
                self.markings[place] = self.markings.get(place, 0) + 1

# test the PetriNet case
# p = PetriNet()

# p.add_place(1)  # add place with id 1
# p.add_place(2)
# p.add_place(3)
# p.add_place(4)
# p.add_transition("A", -1)  # add transition "A" with id -1
# p.add_transition("B", -2)
# p.add_transition("C", -3)
# p.add_transition("D", -4)

# p.add_edge(1, -1)
# p.add_edge(-1, 2)
# p.add_edge(2, -2).add_edge(-2, 3)
# p.add_edge(2, -3).add_edge(-3, 3)
# p.add_edge(3, -4)
# p.add_edge(-4, 4)

# by default all transitions should be disabled
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.add_marking(1)  # add one token to place id 1
# transition A should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-1)  # fire transition A
# # transition B and C should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-3)  # fire transition C
# # transition D should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-4)  # fire transition D
# # no transition should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.add_marking(2)  # add one token to place id 2
# # transition B should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-2)  # fire transition B
# # transition D should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-4)  # fire transition D
# # no transition should be enabled now
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# # by the end of the execution there should be 2 tokens on the final place
# print(p.get_tokens(4))