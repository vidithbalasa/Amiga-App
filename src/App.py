from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial

import rospy
from sensor_msgs.msg import JointState

class SarBotApp(App):
    sliders = ["joint2_to_joint1", "joint3_to_joint2", "joint4_to_joint3", 
            "joint5_to_joint4", "joint6_to_joint5", "joint6output_to_joint6"]
    default_value = 0.0
    max_value = 3
    min_value = -3
    refresh_rate = 0.1 #seconds

    prev_joint_positions = [0] * 6

    def build(self):
        # Initialize ROS node and publisher
        rospy.init_node('kivy_joint_states_publisher', anonymous=True)
        self.pub = rospy.Publisher('/joint_states', JointState, queue_size=10)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create 6 sliders
        self.slider_widgets = []
        for slider_name in self.sliders:
            slider = Slider(min=self.min_value, max=self.max_value, value=self.default_value)
            slider_label = Label()
            self.update_value_label(slider_name, slider_label, slider, slider.value)

            layout.add_widget(slider_label)
            layout.add_widget(slider)

            slider.bind(value=partial(self.update_value_label, slider_name, slider_label))
            self.slider_widgets.append(slider)

        reset_button = Button(text='Reset', size_hint=(1, 2.5))
        reset_button.bind(on_press=self.reset_sliders)
        layout.add_widget(reset_button)

        self.publish_joint_states()

        Clock.schedule_interval(lambda dt: self.publish_joint_states(), self.refresh_rate)

        return layout

    def reset_sliders(self, instance):
        for slider in self.root.children[:-1]:
            slider.value = self.default_value

    def update_value_label(self, slider_name, value_label, slider, value):
        value_label.text = f'{slider_name}          Value: {value:.2f}'
        self.publish_joint_states()

    def publish_joint_states(self):
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = self.sliders
        joint_state.velocity = [round(abs(x.value-y)/self.refresh_rate, 2) for x,y in zip(self.slider_widgets, self.prev_joint_positions)]
        joint_state.position = [slider.value for slider in self.slider_widgets]
        self.prev_joint_positions = joint_state.position
        joint_state.effort = []

        rospy.loginfo(joint_state)
        self.pub.publish(joint_state)

if __name__ == '__main__':
    SarBotApp().run()
