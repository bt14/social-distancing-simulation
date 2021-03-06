import pygame

# this file contains the Button and ButtonSet classes

class Button:

	def __init__ (self, x, y, width, height, text, font, text_color, idle_color, hover_color, callback_funct, visible=True):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.rect = pygame.Rect(x, y, width, height)

		self.text = text
		self.font = font
		self.text_color = text_color
		self.updateLabel()

		self.idle_color = idle_color
		self.hover_color = hover_color
		self.callback_funct = callback_funct
		self.hovered = False
		self.outlineRect = (x-1, y-1, width+2, height+2)
		self.outlineColor = (0,0,0)  
		self.visible = visible

	def updateHover(self, mouse_pos):
		self.hovered = False
		if self.rect.collidepoint(mouse_pos):
			self.hovered = True

	# checks if it was clicked
	def get_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.hovered and self.visible:
				self.callback_funct()
				return True
		return False

	def updateLabel(self):
		self.label = self.font.render(self.text, True, self.text_color)
		self.label_rect = self.label.get_rect(center=self.rect.center)

	def draw(self, win):
		if self.hovered:
			color = self.hover_color
		else:
			color = self.idle_color

		pygame.draw.rect(win, self.outlineColor, self.outlineRect)  
		pygame.draw.rect(win, color, self.rect)
		win.blit(self.label, self.label_rect)


class ButtonSet:

	def __init__ (self, buttons, normal_idle_c, normal_hover_c, select_idle_c, select_hover_c, errorLbl, errorMsgPos):
		
		self.buttons = buttons
		self.normal_idle_c = normal_idle_c
		self.normal_hover_c = normal_hover_c
		self.select_idle_c = select_idle_c
		self.select_hover_c = select_hover_c
		self.selected = False
		self.selectedVal = None	# set by the buttons' callback functions
		self.error = False
		self.errorLbl = errorLbl
		self.errorMsgPos = errorMsgPos

	def draw(self, win):
		if self.error:
			win.blit(self.errorLbl, self.errorMsgPos)

		for button in self.buttons:
			button.draw(win)

	def get_event(self, event):
		for button in self.buttons:
			clicked = button.get_event(event)
			if clicked:
				if button.idle_color == self.normal_idle_c:
					self.buttonSelected(button)
				else:
					self.buttonDeselected(button)

	def buttonSelected(self, button):
		self.selected = True
		self.error = False
		button.idle_color = self.select_idle_c
		button.hover_color = self.select_hover_c
		for button2 in self.buttons:
			if button2 != button:
				button2.idle_color = self.normal_idle_c
				button2.hover_color = self.normal_hover_c

	def buttonDeselected(self, button):
		self.selected = False
		button.idle_color = self.normal_idle_c
		button.hover_color = self.normal_hover_c
