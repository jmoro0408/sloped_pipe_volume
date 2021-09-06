import numpy as np


def calculate_tilt_angle(initial_grade_percent):
    tilt_angle = np.arctan(initial_grade_percent / 100)
    tilt_angle = np.degrees(tilt_angle)
    return tilt_angle


def calculate_pipe_upper_invert(pipe_invert_elev, tilt_angle, pipe_length):
    pipe_upper_invert = np.tan(np.radians(tilt_angle)) * pipe_length + pipe_invert_elev
    return pipe_upper_invert


def calculate_upper_liquid_level(lower_liquid_level, tilt_angle, pipe_length):
    upper_liquid_level = lower_liquid_level
    return upper_liquid_level


def calculate_tilt_angle(initial_grade_percent):
    tilt_angle = np.arctan(initial_grade_percent / 100)
    tilt_angle = np.degrees(tilt_angle)

    return tilt_angle


def calculate_pipe_upper_invert(pipe_invert_elev, tilt_angle, pipe_length):
    pipe_upper_invert = np.tan(np.radians(tilt_angle)) * pipe_length + pipe_invert_elev
    return pipe_upper_invert


def calculate_upper_liquid_level(lower_liquid_level, tilt_angle, pipe_length):
    upper_liquid_level = lower_liquid_level
    return upper_liquid_level


def calculate_total_pipe_volume(pipe_diameter, pipe_length):
    pipe_cross_sectional_area = np.pi / 4 * (pipe_diameter ** 2)
    total_volume = pipe_cross_sectional_area * pipe_length
    total_volume = round(total_volume, 2)
    return total_volume


def calculate_sloped_pipe_volume(
    pipe_diameter, tilt_angle, pipe_length, relative_lower_liquid_level
):
    if tilt_angle == 0:
        tilt_angle = 0.001  # angle of zero breaks the np.tan function, so making a close approximation
    pipe_radius = pipe_diameter / 2
    tilt_angle_radians = np.radians(tilt_angle)
    _h0 = relative_lower_liquid_level - (pipe_length * np.tan(tilt_angle_radians))

    # "normal" case, where both ends have some liquid
    if _h0 >= 0:
        _lf = pipe_length

    # upper end has no liquid - liquid does not reach end of pipe
    elif _h0 < 0:
        # lower_liquid_level = 0
        _lf = pipe_length + _h0 / np.tan(tilt_angle_radians)
        _h0 = 0
        # assert _lf < pipe_length, "Liquid fill length cannot be greater than pipe length"

    _h1 = _h0 + _lf * np.tan(tilt_angle_radians)
    full_volume = None
    # Case where pipe is (at least) partially completely full.
    if _h1 > pipe_diameter:
        _lt = (_h1 - pipe_diameter) / np.tan(tilt_angle_radians)
        full_volume = np.pi * pipe_radius ** 2 * _lt
    else:
        _lt = 0

    _pipe_length = _lf - _lt

    _k = 1 - (_h0 / pipe_radius)
    _c = _k - ((_pipe_length * np.tan(tilt_angle_radians)) / pipe_radius)

    assert -1 <= _k <= 1, "k out of range"
    assert -1 <= _c <= 1, "c out of range"

    integral0 = pipe_radius ** 3 / np.tan(tilt_angle_radians)
    integral1 = _k * np.arccos(_k)
    integral2 = (1 / 3) * (np.sqrt(1 - (_k ** 2))) * (_k ** 2 + 2)
    integral3 = _c * np.arccos(_c)
    integral4 = (1 / 3) * (np.sqrt(1 - (_c ** 2))) * (_c ** 2 + 2)
    volume = integral0 * (integral1 - integral2 - integral3 + integral4)

    if (pipe_radius == relative_lower_liquid_level) and (
        tilt_angle == 0
    ):  # Pipe is exactly half full and no slope
        volume = (pipe_length * np.pi * pipe_radius ** 2) / 2
    if full_volume is not None:
        volume = volume + full_volume

    return volume


# initial values
initial_grade_percent = 0.1  # inital grade value
maximum_grade_value = 2  # maximum grade (%) to plot
pipe_length = 50
pipe_diameter = 2
pipe_invert_start = 1  # pipe invert at pipe end
lower_liquid_level = 3  # liquid level at pipe end

relative_lower_liquid_level = np.abs(pipe_invert_start - lower_liquid_level)

no_points_to_plot = 100
no_grades = np.arange(0, maximum_grade_value, 20)
pipe_chainage = np.linspace(0, pipe_length, no_points_to_plot).tolist()
pipe_chainage = [round(elem) for elem in pipe_chainage]


tilt_angle = calculate_tilt_angle(initial_grade_percent)


test_grades = np.linspace(0, 5, 10)

for i in test_grades:
    sloped_volume = calculate_sloped_pipe_volume(
        pipe_diameter, i, pipe_length, relative_lower_liquid_level
    )
    print(sloped_volume)
