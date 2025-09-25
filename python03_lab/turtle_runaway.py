# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, math

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=40):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('#3f48cc')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('#ed1c24')
        self.chaser.penup()

        # Initiate check catched
        self.catched = turtle.RawTurtle(canvas)
        self.catched.hideturtle()
        self.catched.penup()
        
        self.timer = turtle.RawTurtle(canvas)
        self.timer.hideturtle()
        self.timer.penup()

    def respawn_runner(self, margin=320):
        xmin, xmax = int(-min(margin, self.half_w-5)), int(min(margin, self.half_w-5))
        ymin, ymax = int(-min(margin, self.half_h-5)), int(min(margin, self.half_h-5))
        
        x = random.randint(xmin, xmax)
        y = random.randint(ymin, ymax)
        
        self.runner.penup()
        self.runner.setpos(x, y)
        self.runner.setheading(random.randint(0,359))
    
    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        
        self.count_timer = 300.0
        self.catched_runners = 0
        
        # TODO) You can do something here and follows.
        # variable declare
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        # screen info
        self.half_w = self.canvas.window_width() / 2
        self.half_h = self.canvas.window_height() / 2
        self.edge = 20.0  # check dist from edge
    
    def step(self):
        # TODO) You can do something here and follows.
         # Game Over setting
        if self.count_timer <= 0:
            self.count_timer = 0.0  # set counter 0.0
            # final draw
            self.catched.clear()
            self.catched.setpos(-300, 300)
            self.catched.write(f'catched {self.catched_runners} runners', font=('Arial', 24, 'bold'), )

            self.timer.clear()
            self.timer.setpos(150, 300)
            self.timer.write(f'time: {round(self.count_timer,1)}sec', font=('Arial', 24, 'bold'))

            # draw Game over
            self.catched.setpos(-90, 0)
            self.catched.write('GAME OVER', font=('Arial', 36, 'bold'))

            # key solve
            self.canvas.onkeypress(None, 'Up')
            self.canvas.onkeypress(None, 'Down')
            self.canvas.onkeypress(None, 'Left')
            self.canvas.onkeypress(None, 'Right')

            return  # ontimer 재등록 없이 종료
        
        # updates
        self.count_timer -= 1/10 # 1 msec
        self.runner.run_ai(self.chaser.pos())
        
        runner_x, runner_y = self.runner.pos()
        chaser_x, chaser_y = self.chaser.pos()
        
        # check edge of runner
        if abs(runner_x) > self.half_w - self.edge or abs(runner_y) > self.half_h - self.edge:
            self.respawn_runner()
            
        # check edge of chaser
        chaser_x = min(chaser_x, self.half_w - self.edge)            # 오른쪽 경계
        chaser_x = max(chaser_x, -self.half_w + self.edge)           # 왼쪽 경계
        chaser_y = min(chaser_y, self.half_h - self.edge)            # 위쪽 경계
        chaser_y = max(chaser_y, -self.half_h + self.edge)           # 아래쪽 경계
        self.chaser.setpos(chaser_x, chaser_y)
     
        # check catched and respawn runner
        if self.is_catched():
            self.catched_runners += 1
            self.runner.step_move += 2
            self.runner.step_turn += 2
            self.respawn_runner()
        
        # draw catched text
        self.catched.undo()
        self.catched.penup()
        self.catched.setpos(-300, 300)
        self.catched.write(f'catched {self.catched_runners} runners') 
               
        # draw timer text
        self.timer.undo()
        self.timer.penup()
        self.timer.setpos(280,300)
        self.timer.write(f'time: {round(self.count_timer,1)}sec')

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        
        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()
             

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos):
        x, y = self.pos()
        ox, oy = opp_pos

        # run away from opp
        angle_to_opp = math.degrees(math.atan2(oy - y, ox - x))
        angle_away = (angle_to_opp + 180.0) % 360.0

        # [-180, 180] normalization
        delta = (angle_away - self.heading() + 540.0) % 360.0 - 180.0

        # randomly move or turn
        mode = random.randint(0,1)
        if mode == 0:
            if delta>0:
                self.left(self.step_turn)
            else:
                self.right(self.step_turn)
        else:
            self.forward(self.step_move)


if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title("Turtle Runaway")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgpic("background.png")

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
