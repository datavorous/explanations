'''
This will be like an exercise where I try to explain binary trees in an intuitive manner.
I like to imagine them as spherical hollow candies joined with each other using sticks , based on certain predefined rule(s).

Hollow candies .. so we can store inside them .. information to fill up the spaces.
Candies <-> Nodes
Sticks <-> Edges 
'''
class Node:
    def __init__(self, value: int):
        '''
        This is the Node class, i.e. our candies.
        What do we have here hmmm...
        I wish to store an integer 'value' inside each candy
        That will allow us to organize them.
        
        We store references to neighbouring candies as well
        (we ask the other candies, to let us know about their position(s)),
        after that's done, we can now place the chopsticks properly.
        so, knowing our own position is a must, to make sure we can answer.
        
        This self.pos aint requried but .. imagining in terms of our physical world feels better
        than an abstract form of establishing and defining connections.
        '''
        self.value = value
        self.left = None
        self.right = None
        self.pos = (0, 0)
        # we keep the pos (0,0) initially
        # this will be edited later, once we are aware of the total number of candies which we will need


class BinaryTree:
    '''
    This class will enforce rules to connect the candies with each others.
    We define the root i.e. the first candy, which will hold the rest of the structure.
    '''
    def __init__(self):
        self.root = None

    '''
    Wrapper method to execute the recursive function
    1. You dont understand what recursion is? Read line 2.
    2. Understand recursion
    '''
    def insert(self, value):
        # IS THERE ANY ROOT CANDY PRESENT???
        # NO? THEN LET'S MAKE THIS CANDY THE ROOT OF THIS MEGA-CANDY STRUCTURE
        if not self.root:
            self.root = Node(value)
        # IF IT IS ALREADY THERE THEN WE NEED TO JUMP ELSEWHERE TO ENFORCE some RULES
        # LET'S SAY THE ROOT NODE IS [1, ROOT]
        
        else:
            # Also providing the self.root's pos, because we can not position ourself
            # without knowing what had happened before
            self._insert(self.root, value)

    def _insert(self, node, value):
        # balancing
        # let us balance this
        # is the value that we are given (ie the one we have not placed yet)
        if value < node.value:
            # if there is a left node already, then let's pick it up
            # and try to find the one which is in left of it
            # and so on and so forth
            # once found we attach it
            # it might happen that left -> left -> right 
            # or it might happen a left -> left etc 
            # drawing it on a piece of paper would be really good for understanding
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = Node(value)
        else:
            if node.right:
                # same thing as above
                self._insert(node.right, value)
            else:
                node.right = Node(value)


# now here is my data
# we sequentially feed each data as a candy
# and by some alien ritual it gets arranged automatically
data = [4, 2, 6, 1, 3, 5, 7]

bt = BinaryTree()
for x in data:
    bt.insert(x) # done feeding 


'''
this part aint really necessary but i wish to render these candies on the screen
i have to do something which makes sure there is sufficient space between the candies
in each level and between each level
'''

def align(bt: BinaryTree, x_gap=100, y_gap=100) -> None:
    counter = 1
    '''
    yes yes depth first search
    we take a candy structure 
    we go to the left
    we go to the left of left
    we continue till there is nothing left
    now we check our immediate right
    we go above 
    now we repeat the conditional traversal again and again till we reach the call stack of the root candy
    and start our journey to the right of the root candy
    '''
    def dfs(node: Node, depth):
        
        nonlocal counter
         
        if node is None: ## hm this is the base case let's deal with it later ... (1)
            return
        
        dfs(node.left, depth + 1) # let's go to our left of depth 1+1 = 2 ... get back to the above comment marked as (1), if not that,
        # then we go left again
        # say, we hit the bottom, what do we do now?
        # ofcourse jump back to our previous callstacks
        # then it starts the immediate right ones
        # by now we have accumulated a lot of depth 
        # let's assign our candies some coordinates
        
        
        '''
        this part is crucial
        first we go to the left most part of the tree
        then we increment this x counter sequentially
        
               5
              / \
             2   8
            / \   \
           1   3   9
                
        aaa let's say we are in 5
        now we go to 2
        then we go to 1
        we reach the dead end at None
        now we are at 1
        we increment counter_x 
        conveyer belt shifted right
        now we go above 
        we see depth of previous - 1 but conveyer_x gets +1

        now we get back to right aka 3
        depth += 1 again and similarly counter += 1 
        dead end again, nothing in right or left
    
        '''
        
        x = counter * x_gap # this thing increases everytime we assign a candy
        y = depth * y_gap # this thing increases everytime we go far and far below
        
        node.pos = (x, y)
        counter += 1 # yay one day, increase the counter!
        
        dfs(node.right, depth + 1) # well let's go right
        
        # i think ill draw something to make it clear
        # or just animate it
        
    dfs(bt.root, 1) # ahhh recursion,let's enter, shall we? starting with the root candy and a depth of 1.
    
align(bt, 50, 100) # done aligning, offset is needed, but ill skip it for now


#### poing poing poing

import pygame
import sys

pygame.init()
input_text = ""
input_pos = (10, 10)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("poing poing")
font = pygame.font.SysFont("Helvetica", 25)
clock = pygame.time.Clock()
## basic boilerplate 


def render_tree(screen, node, font):
    '''
    this function is very much self explanatory
    you take a candy
    check the left of it
    if it exists
    draw a line
    
    in the place of the candy in hand
    draw circles
    and render some text font to mention the value
    '''
    if node is None:
        return
    if node.left:
        pygame.draw.line(screen, (235, 172, 162), node.pos, node.left.pos, 5)
        render_tree(screen, node.left, font)
    if node.right:
        pygame.draw.line(screen, (235, 172, 162), node.pos, node.right.pos, 5)
        render_tree(screen, node.right, font)

    pygame.draw.circle(screen, (206, 106, 107), node.pos, 30)
    pygame.draw.circle(screen, (235, 172, 162), node.pos, 30, 5)
    text = font.render(str(node.value), True, (235, 252, 232))
    text_rect = text.get_rect(center=node.pos)
    screen.blit(text, text_rect)

running = True
while running:
    screen.fill((255, 241, 213))
    input_surf = font.render(f"Insert: {input_text}", True, (50,50,50))
    screen.blit(input_surf, input_pos)
    # recursive way of rendering
    # check above commented function for understanding
    render_tree(screen, bt.root, font)
    pygame.display.flip()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    val = int(input_text)
                    bt.insert(val)
                    align(bt, 50, 100)
                except ValueError:
                    pass
                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            else:
                char = event.unicode
                if char.isdigit() or (char == "-" and len(input_text)==0):
                    input_text += char


pygame.quit()
sys.exit()
