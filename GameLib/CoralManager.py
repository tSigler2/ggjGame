from Coral import Coral


class CoralManager:
    """
    The CoralManager class manages all coral instances in the game.
    It handles spawning, updating, and removing corals.
    """

    def __init__(self, game):
        """
        Initialize the coral manager.

        Args:
            game: The main game object.
        """
        self.game = game
        self.corals = []  # List of active coral instances

    def add_coral(
        self,
        health: int,
        coords: tuple,
        damage: int,
        path: str,
        animation_time: int,
        *animation_sets
    ):
        """
        Add a new coral to the game.

        Args:
            health: The coral's initial health.
            coords: The coral's grid coordinates (x, y).
            damage: The damage dealt by the coral per attack.
            path: Base path for animation assets.
            animation_time: Time between animation frames.
            *animation_sets: Animation sets (e.g., "std").
        """
        coral = Coral(
            game=self.game,
            health=health,
            coords=coords,
            damage=damage,
            path=path,
            animation_time=animation_time,
            *animation_sets,
        )
        self.corals.append(coral)
        self.game.map[coords[0]][coords[1]].occupied = True
        self.game.map[coords[0]][coords[1]].occupant = coral

    def remove_coral(self, coral):
        """
        Remove a coral from the game.

        Args:
            coral: The coral instance to remove.
        """
        if coral in self.corals:
            self.corals.remove(coral)
            self.game.map[coral.coords[0]][coral.coords[1]].occupied = False
            self.game.map[coral.coords[0]][coral.coords[1]].occupant = None

    def update_corals(self):
        """
        Update all active corals in the game.
        """
        corals_to_remove = []
        for coral in self.corals:
            coral.update()
            if coral.health <= 0:
                corals_to_remove.append(coral)

        # Remove dead corals
        for coral in corals_to_remove:
            self.remove_coral(coral)

    def move_coral(self, coral, new_coords: tuple):
        """
        Move a coral to new grid coordinates.

        Args:
            coral: The coral instance to move.
            new_coords: New grid coordinates (x, y).
        """
        if coral in self.corals:
            coral.move(new_coords)
