import tkinter as tk
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake body at top-left corner
        for i in range(self.body_size):
            self.coordinates.append([0, 0])

        # Draw initial squares
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = self.random_position()
        x, y = self.coordinates

        # Draw the food as an oval
        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

    def random_position(self):
        """Generate a random position aligned with the grid."""
        max_x = (GAME_WIDTH // SPACE_SIZE) - 1
        max_y = (GAME_HEIGHT // SPACE_SIZE) - 1
        x = random.randint(0, max_x) * SPACE_SIZE
        y = random.randint(0, max_y) * SPACE_SIZE
        return [x, y]

class Game:
    def __init__(self, root):
        self.root = root
        self.score = 0
        self.direction = 'down'
        self.speed = 200  # ms

        root.title("Snake game")
        root.resizable(False, False)

        self.label = tk.Label(root, text=f"Score: {self.score}", font=('consolas', 40))
        self.label.pack()

        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Center the window on the screen
        self.root.update()
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bind arrow keys
        root.bind('<Left>', lambda event: self.change_direction('left'))
        root.bind('<Right>', lambda event: self.change_direction('right'))
        root.bind('<Up>', lambda event: self.change_direction('up'))
        root.bind('<Down>', lambda event: self.change_direction('down'))

        # Create the snake and the food
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        # Start the game loop
        self.next_turn()

    def next_turn(self):
        """Called periodically to update game state and refresh the screen."""
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        # Insert new coordinates at the front of the snake body
        self.snake.coordinates.insert(0, (x, y))

        # Draw a new rectangle for the head
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=SNAKE_COLOR, tag="snake"
        )
        self.snake.squares.insert(0, square)

        # Check if we have collided with the food
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            # Remove old food and create a new one
            self.canvas.delete("food")
            self.food = Food(self.canvas)

            # Optional: Increase speed slightly each time
            # self.speed = max(50, self.speed - 5)

        else:
            # Remove the last part of the snake's tail
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Check collisions
        if self.check_collisions():
            self.game_over()
        else:
            # Schedule next update
            self.root.after(self.speed, self.next_turn)

    def change_direction(self, new_direction):
        """Update direction if it's not the direct opposite."""
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        """Return True if the snake collides with itself or boundaries."""
        x, y = self.snake.coordinates[0]

        # Check boundary collision
        if x < 0 or x >= GAME_WIDTH:
            return True
        if y < 0 or y >= GAME_HEIGHT:
            return True

        # Check self collision
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        """Handle game over state."""
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            font=('consolas', 70),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )
        # Optionally, you can unbind arrow keys or provide a restart mechanism.

def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
