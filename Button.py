import pygame

class Button:
    """This class contains all settings related to the button.

    """
    def __init__(self, x, y, width, height, text, color_normal, color_hover, font_normal, font_hover):
        """__init__ method for button class

        Args:
            x (int): x coordinate value for the start of button - top left corner.
            y (int): y coordinate value for the start of button - top left corner.
            width (int): width of the button.
            height (int): height of the button.
            text (str): display text inside button.
            color_normal (<class 'tuple'>): RGBA color value of the button in the format (R, G, B, A) when mouse not hover.
            color_hover (<class 'tuple'>): RGBA color value of the button in the format (R, G, B, A) when mouse hover.
            font_normal (pygame.font.Font): Button font when not mouse hover
            font_hover (pygame.font.Font): Button font on mouse hover.

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.font_normal = font_normal
        self.font_hover = font_hover

    def is_mouse_hover(self):
        """Button class method to return if mouse hover on button. 

        Returns:
            mouse_hover (bool): True if mouse hover, False otherwise.

        """
        button_x1 = self.x
        button_x2 = self.x + self.width
        button_y1 = self.y
        button_y2 = self.y + self.height
        
        mouse_hover = False

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_x > button_x1 and mouse_x < button_x2 and mouse_y > button_y1 and mouse_y < button_y2:
            mouse_hover = True
        
        return mouse_hover

    def is_mouse_clicked(self):
        """Button class method to return if mouse clicked on button. 

        Returns:
            mouse_clicked (bool): True if mouse clicked, False otherwise.

        """
        mouse_clicked = False
        if self.is_mouse_hover() and pygame.mouse.get_pressed()[0]:
            mouse_clicked = True
        
        return mouse_clicked

    def show(self, window):
        """Button class method to show/display button.

        Args:
            window (<class 'pygame.Surface'>): surface to display button.
        
        """
        # setting button color and font for when mouse not hover
        if self.is_mouse_hover() == False:
            button_color = self.color_normal
            button_font = self.font_normal

        # setting button color and font for when mouse hover  
        else:
            button_color = self.color_hover
            button_font = self.font_hover

        # Rendering button and text on the window
        self.render_button(window, button_color)
        self.render_text(window, button_font)

    def render_button(self, window, button_color, radius=0.4):
        """Button class method to draw rounded rectangle. 

        Args:
            window (<class 'pygame.Surface'>): surface to draw filled rouded rectangle .
            rect (<class 'pygame.Rect'>): pygame.Rect object.
            button_color (<class 'tuple'>): RGBA color value of the button in the format (R, G, B, A).
            radius (float): corner radius value between 0 and 1.

        """
        rect = pygame.Rect(self.rect)
        color = pygame.Color(*button_color)
        rect_pos = rect.topleft
        rect.topleft = 0,0
        rectangle = pygame.Surface(rect.size,pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
        pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
        circle = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

        # radius circle rendering top left
        radius = rectangle.blit(circle,(0,0))
        # radius circle rendering top right
        radius.topright = rect.topright
        rectangle.blit(circle,radius)
        # radius circle rendering bottom right
        radius.bottomright = rect.bottomright
        rectangle.blit(circle,radius)
        # radius circle rendering bottom left
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle,radius)

        rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
        rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

        rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255,255,255),special_flags=pygame.BLEND_RGBA_MIN)

        window.blit(rectangle, rect_pos)

    def render_text(self, window, button_font):
        """Button class method to draw text. 

        Args:
            window (<class 'pygame.Surface'>): surface to draw filled rouded rectangle .
            button_font (pygame.font.Font): Button font to draw.

        """

        text = button_font.render(self.text, False, (0, 0, 0))
        text_width, text_height = text.get_rect().size
        textpos = (self.x + (self.width - text_width)/2, self.y + ((self.height - text_height)/2))
        window.blit(text,textpos)

        
        
