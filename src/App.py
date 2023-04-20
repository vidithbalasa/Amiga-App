from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial


class MyApp(App):
	sliders = ['joint2_to_joint1'] + [str(x) for x in range(2,7)]

	def build(self):
		layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

		# Create 6 sliders
		for slider_name in self.sliders:
			slider = Slider(min=-3, max=3, value=1)
			slider_label = Label()
			self.update_value_label(slider_name, slider_label, slider, slider.value)

			layout.add_widget(slider_label)
			layout.add_widget(slider)

			slider.bind(value=partial(self.update_value_label, slider_name, slider_label))

		reset_button = Button(text='Reset', size_hint=(1, 2.5))
		reset_button.bind(on_press=self.reset_sliders)
		layout.add_widget(reset_button)

		return layout

	def reset_sliders(self, instance):
		for slider in self.root.children[:-1]:
			slider.value = 1

	def update_value_label(self, slider_name, value_label, slider, value):
		value_label.text = f'{slider_name}          Value: {value:.2f}'


if __name__ == '__main__':
    MyApp().run()
