from manimlib.imports import *
import numpy as np

class BareOscilator(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_axis_width": FRAME_WIDTH,
        "y_min": 0,
        "y_max": 30,
        "y_axis_height": FRAME_HEIGHT * 0.7,
        "y_tick_frequency": 5,
        "graph_origin": BOTTOM + UP,
        "y_axis_label": "$U$",
        "x_extreme_complete_min": -6,
        "x_extreme_complete_max": 6,
        "x_extreme_osc_min": -4,
        "x_extreme_osc_max": 4,
        "run_time_def": 5,
        "loops": 2,
    }
    def initialize(self):
        pass
    def U(self, x):
        return 0.0
    def X(self, x):
        return 0.0
    def construct(self):
        self.setup_axes(animate=False)
        self.initialize()
        funcs=(('X', self.X), ('U', self.U))
        path_complete=self.get_graph(self.U, x_min=self.x_extreme_complete_min, x_max=self.x_extreme_complete_max) 
        E = self.U(self.x_extreme_osc_min)
        energy_line=self.get_graph(lambda x: E) 
        paths={}
        for label, fnc in funcs:
            paths[label]={
                'dot': Dot(self.coords_to_point(self.x_extreme_osc_min,self.U(self.x_extreme_osc_min))),
                'forward': self.get_graph(fnc, x_min=self.x_extreme_osc_min, x_max=self.x_extreme_osc_max), 
                'backwards': self.get_graph(fnc, x_min=self.x_extreme_osc_max, x_max=self.x_extreme_osc_min)
                } 
        self.play(ShowCreation(path_complete),
            ShowCreation(energy_line))
        for label, fnc in funcs:
            ShowCreation(paths[label]['dot'])
        for loop in range(self.loops):
            for direction in ['forward', 'backwards']:
                self.play(MoveAlongPath(paths['U']['dot'], paths['U'][direction]),
                    MoveAlongPath(paths['X']['dot'], paths['X'][direction]),
                    run_time=self.run_time_def)


class SimpleHarmonicOscilator(BareOscilator):
    CONFIG = {
        'k': 1.0,
        'loops': 4
        }
    def U(self, x):
        return 0.5 * self.k* x**2



class QuarticOscilator(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'a': 0.05,
        'b': -0.5,
        'c': 3.0,
        'loops': 4,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  


class QuarticOscilatorR(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'x_extreme_osc_min': 0,
        'a': 0.08,
        'b': -1.5,
        'c': 10.0,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  
    def initialize(self):
        self.x_extreme_osc_max = (-self.b/self.a)**0.5

class QuarticOscilatorArb(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'x_extreme_osc_min': 1.0,
        'a': 0.08,
        'b': -1.5,
        'c': 10.0,
        'loops': 4,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  
    def initialize(self):
        E=self.U(self.x_extreme_osc_min)
        self.x_extreme_osc_max = np.sqrt((-self.b+ np.sqrt(self.b**2-4*self.a*(self.c-E)))/(2*self.a))

class QuarticOscilatorSmall(QuarticOscilatorArb):
    CONFIG = {
        "x_min": 0,
        "x_max": 6,
        "graph_origin": 2.5 * DOWN + 5 * LEFT,
        }
    def initialize(self):
        x_mini=np.sqrt(-self.b/(2*self.a))
        eps=0.2
        self.x_extreme_osc_min=x_mini*(1-eps)
        def Uapprox(x):
            return self.U(x_mini)-2*self.b*(x-x_mini)**2
        path_approx=self.get_graph(Uapprox, x_min=self.x_extreme_complete_min, x_max=self.x_extreme_complete_max)
        self.play(ShowCreation(path_approx))
        super().initialize()

class ParametricOscilator(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_axis_width": FRAME_WIDTH,
        "y_min": 0,
        "y_max": 30,
        "y_axis_height": FRAME_HEIGHT * 0.7,
        "y_tick_frequency": 5,
        "graph_origin": BOTTOM + UP,
        "y_axis_label": "$U$",
        "x_extreme_complete_min": -6,
        "x_extreme_complete_max": 6,
        "x_extreme_osc_min": -4,
        "x_extreme_osc_max": 4,
        "run_time_def": 5,
        "loops": 2,
    }
    def initialize(self):
        pass
    def U(self, x):
        return 0.0
    def X(self, t):
        return 0.0
    def parametric_fnct_U(self,t):
        x=self.X(t)
        y=self.U(x)
        if not np.isfinite(y):
            y = self.y_max
        return self.coords_to_point(x,y)
    def parametric_fnct_X(self,t):
        x=self.X(t)
        y=0
        return self.coords_to_point(x,y)
    def construct(self):
        self.setup_axes(animate=False)
        self.initialize()
        funcs=(('X', self.X), ('U', self.U))
        path_complete=self.get_graph(self.U, x_min=self.x_extreme_complete_min, x_max=self.x_extreme_complete_max) 
        E = self.U(self.x_extreme_osc_min)
        energy_line=self.get_graph(lambda x: E) 
        paths={}
        # for label, fnc in funcs:
        #     paths[label]={
        #         'dot': Dot(self.coords_to_point(self.x_extreme_osc_min,self.U(self.x_extreme_osc_min))),
        #         'forward': self.get_graph(fnc, x_min=self.x_extreme_osc_min, x_max=self.x_extreme_osc_max), 
        #         'backwards': self.get_graph(fnc, x_min=self.x_extreme_osc_max, x_max=self.x_extreme_osc_min)
        #         } 
        dotX = Dot(self.coords_to_point(self.x_extreme_osc_min,0))
        dotU = Dot(self.coords_to_point(self.x_extreme_osc_min,self.U(self.x_extreme_osc_min)))
        color = next(self.default_graph_colors_cycle)
        pathX = ParametricFunction(self.parametric_fnct_X)
        pathU = ParametricFunction(self.parametric_fnct_U)
        self.play(ShowCreation(path_complete),
            ShowCreation(energy_line),
            ShowCreation(dotX),
            ShowCreation(dotU))         
        self.play(
            MoveAlongPath(dotU, pathU, rate_func=linear),
            MoveAlongPath(dotX, pathX, rate_func=linear),
            run_time=self.run_time_def)


class SimpleHarmonicOscilatorDamped(ParametricOscilator):
    CONFIG = {
        'k': 1.0,
        #'omega': 1.0,
        'phi': 0.0,
        'tau': 1.0,  # damping time
        'run_time_def': 50,
        'loops': 5,
        }
    def U(self, x):
        return 0.5 * self.k* x**2
    def X(self,t):
        return self.x_extreme_osc_min * np.exp(-t/self.tau) * np.cos(self.loops*t*2*PI+self.phi)


class point_and_shadow(Dot):
    CONFIG = {
        "fill_color": RED,
        "fill_opacity": 1, 
        'radius': 0.2,
        'text_x': '$x=A\\cos(%s)$',
        'text_y': '$y=A\\sin(%s)$',
        'text_z': '$z=Ae^{i(%s)}$',
        'text_arc': '%s',
        'phi_t_str': '\\omega_0 t',
    }
    def __init__(self, point=ORIGIN, phi0=0, **kwargs):
        super().__init__(point=point, **kwargs)
        if phi0 != 0:
            self.phi_t_str=self.phi_t_str+'+\varphi'
        self.text_x = self.text_x % (self.phi_t_str)
        self.text_y = self.text_y % (self.phi_t_str)
        self.text_z = self.text_z % (self.phi_t_str)
        self.text_arc = '$%s$' % (self.phi_t_str)
    def get_shadows(self):
        x,y = self.get_x(), self.get_y()
        x_p =  Dot((x,0,0), name='x_shadow', color=BLUE, radius=0.2) 
        y_p = Dot((0,y,0), name='y_shadow', color=BLUE, radius=0.2)
        r_v = Vector((x,y,0), name='r_vector', color=RED_A)
        angle = r_v.get_angle()
        if angle<0 :
            angle=TAU+angle
        r_arc = Arc(angle=angle, name='r_arc')
        return (
                x_p,
                Line((x,0,0),(x,y,0), name='x_line', color=GREY),
                Vector((x,0,0), name='x_vector', color=BLUE_A),
                TextMobject(self.text_x, name='x_text').next_to(x_p, direction=DOWN),
                y_p,
                Line((0,y,0),(x,y,0),name='y_line', color=GREY),
                Vector((0,y,0), name='y_vector', color=BLUE_A),
                TextMobject(self.text_y, name='y_text').next_to(y_p, direction=UP),
                Line((0,0,0),(x,y,0),name='r_line', color=RED_A),
                r_v,
                TextMobject(self.text_z, name='r_text').next_to(self, direction=RIGHT),
                r_arc,
                TextMobject(self.text_arc, name='r_arc_text').next_to(r_arc.get_end(), direction=RIGHT),
                )
    
class CircleHarmonicOscillator(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 1,
        'y_min': -1,
        'y_max': 1,
        "graph_origin": ORIGIN,
        "x_axis_width": 0.5*FRAME_WIDTH,
        "y_axis_height": 0.5*FRAME_WIDTH,
        'show_objects_list': [
            'x_shadow', 
        #    'x_line',
        #    'x_vector',
        #    'y_shadow',
        #    'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'loops': 2,
        'run_time': 25,
        'phi0': 0,
    }

    def construct(self):
        self.setup_axes()
        point=point_and_shadow(self.coords_to_point(1,0),phi0=self.phi0)
        shadows = point.get_shadows()
        for s in shadows:
            s.fade(darkness=1.0)
        group=VGroup(point, *shadows)
        r=get_norm(point.get_center())
        circle=Circle(radius=r)
        phi=ValueTracker(self.phi0)
        self.add(circle)
        self.add(group)
        show_objects_list=self.show_objects_list
        def update_points(group):
            point, *shadows = group
            point.move_to(circle.point_from_proportion(phi.get_value()%1))
            new_objects = point.get_shadows()
            for obj, new_obj in zip(shadows,new_objects): 
                if obj.name in show_objects_list:
                    obj.become(new_obj)

        group.add_updater(update_points)
        self.play(phi.increment_value, self.loops, run_time=self.run_time , rate_func=linear)

class CircleHarmonicOscillatorX(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
        #    'y_shadow',
            'x_line',
        #    'y_line',
        #    'r_line'
        ]
    }

class CircleHarmonicOscillatorXY(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            # 'r_vector'
        ]
    }

class CircleHarmonicOscillatorAll(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ]
    }
class CircleHarmonicOscillatorAllphi(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ],
        'phi0': 1.0/8.0 
    }

class CircleHarmonicOscillatorXYR(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            # 'x_line',
            'x_vector',
            'y_shadow',
            # 'y_line',
            'y_vector',
            # 'r_line',
            'r_vector',
        ]
    }

class CircleHarmonicOscillatorXYRA(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            'r_vector',
            'r_arc',
            'r_arc_text'
        ]
    }
class CircleHarmonicOscillatorNone(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
        ]
    }

class point_and_shadow_damped(point_and_shadow):
    CONFIG = {
        "fill_color": RED,
        "fill_opacity": 1, 
        'radius': 0.2,
        'text_x': '$x=Ae^{-t/\\tau}\\cos(%s)$',
        'text_y': '$y=Ae^{-t/\\tau}\\sin(%s)$',
        'text_z': '$z=Ae^{-t/\\tau+i(%s)}$',
        'text_arc': '%s',
        'phi_t_str': '\\omega t',
    }

class DampedCircleHarmonicOscillator(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 1,
        'y_min': -1,
        'y_max': 1,
        "graph_origin": ORIGIN,
        "x_axis_width": 0.5*FRAME_WIDTH,
        "y_axis_height": 0.5*FRAME_WIDTH,
        'show_objects_list': [
            'x_shadow', 
        #    'x_line',
        #    'x_vector',
        #    'y_shadow',
        #    'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'loops': 5,
        'run_time': 25,
        'phi0': 0,
        'tau': 1.0,
    }
    def parametric_fnct_spiral(self,t):
        x=np.exp(-t/self.tau) * np.cos(self.loops*t*2*PI+self.phi0)
        y=np.exp(-t/self.tau) * np.sin(self.loops*t*2*PI+self.phi0)
        return self.coords_to_point(x,y)

    def construct(self):
        self.setup_axes()
        point = point_and_shadow_damped(self.coords_to_point(1,0),phi0=self.phi0)
        path = VMobject(color=RED)
        path.set_points_as_corners([point.get_center(),point.get_center()+UP*0.001])
        shadows = point.get_shadows()
        for s in shadows:
            s.fade(darkness=1.0)
        group=VGroup(point, path, *shadows)
        r=get_norm(point.get_center())
        spiral=ParametricFunction(self.parametric_fnct_spiral)
        phi=ValueTracker(self.phi0)
        self.add(group)
        show_objects_list=self.show_objects_list
        def update_points(group):
            point, path, *shadows = group
            point.move_to(spiral.point_from_proportion(phi.get_value()%1))
            new_objects = point.get_shadows()
            for obj, new_obj in zip(shadows,new_objects): 
                if obj.name in show_objects_list:
                    obj.become(new_obj)
            new_path=path.copy()
            new_path.append_vectorized_mobject(Line(new_path.points[-1],point.get_center()))
            new_path.make_smooth()
            path.become(new_path)
        group.add_updater(update_points)
        self.play(phi.increment_value, 1, run_time=self.run_time , rate_func=linear)

class DampedCircleHarmonicOscillatorXYRA(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            'r_vector',
            'r_arc',
            'r_arc_text'
        ]
    }

class DampedCircleHarmonicOscillatorXYR(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
        'x_shadow', 
        'x_line',
        'x_vector',
        'y_shadow',
        'y_line',
        'y_vector',
        # 'r_line',
        'r_vector',
        #'r_arc',
        #'r_arc_text'
        ]
}

class DampedCircleHarmonicOscillatorX(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
        #    'y_shadow',
            'x_line',
        #    'y_line',
        #    'r_line'
        ]
    }

class DampedCircleHarmonicOscillatorXY(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            # 'r_vector'
        ]
    }

class DampedCircleHarmonicOscillatorAll(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ]
    }
class CircleHarmonicOscillatorAllphi(DampedCircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ],
        'phi0': 1.0/8.0 
    }
