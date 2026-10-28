import pytest
from course_registration import can_register, waitlist_position, late_fee


# ================= can_register =================
# Branch: student_status not in MAX_CREDITS (True / False)
def test_can_register_unknown_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("graduate", 10, 4, True)


# Branch: course_credits <= 0 (True / False)
def test_can_register_zero_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_can_register_negative_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -3, True)


# Branch: not prerequisites_met (True / False)
def test_can_register_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


# Branch: current + course > limit (True / False), for every status
def test_can_register_regular_success():
    assert can_register("regular", 20, 4, True) == "registered"


def test_can_register_regular_limit_exceeded():
    assert can_register("regular", 21, 4, True) == "credit limit exceeded"


def test_can_register_probation_exact_limit():
    assert can_register("probation", 12, 4, True) == "registered"


def test_can_register_probation_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


def test_can_register_honors_success():
    assert can_register("honors", 24, 4, True) == "registered"


def test_can_register_honors_limit_exceeded():
    assert can_register("honors", 25, 4, True) == "credit limit exceeded"


# ================= waitlist_position =================
# Branch: capacity <= 0 (True / False)
def test_waitlist_zero_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)


def test_waitlist_negative_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(5, -10, 0)


# Branch: enrolled < capacity (True / False)
def test_waitlist_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_waitlist_last_seat_available():
    assert waitlist_position(39, 40, 0) == 0


# Branch: waitlist_length >= 10 (True / False)
def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_over_full():
    assert waitlist_position(45, 40, 15) == -1


def test_waitlist_one_before_full():
    assert waitlist_position(40, 40, 9) == 10


def test_waitlist_empty_waitlist():
    assert waitlist_position(40, 40, 0) == 1


# ================= late_fee =================
# Branch: days_late <= 0 (True / False)
def test_late_fee_on_time():
    assert late_fee(0, 18, False) == 0


def test_late_fee_early():
    assert late_fee(-2, 18, False) == 0


# Branch: has_waiver (True / False)
def test_late_fee_waiver():
    assert late_fee(5, 18, True) == 0


# Branch: days_late <= 7 (True / False)
def test_late_fee_one_day():
    assert late_fee(1, 18, False) == 500


def test_late_fee_boundary_seven_days():
    assert late_fee(7, 18, False) == 500


def test_late_fee_eight_days():
    assert late_fee(8, 18, False) == 600


def test_late_fee_ten_days():
    assert late_fee(10, 18, False) == 800


# Branch: credits > 20 (True / False)
def test_late_fee_credits_boundary_twenty():
    assert late_fee(5, 20, False) == 500


def test_late_fee_credits_above_twenty():
    assert late_fee(5, 21, False) == 750


# Branch: fee > 2000 (True / False)
def test_late_fee_exactly_cap_not_exceeded():
    # 500 + 15*100 = 2000 -> not greater than 2000
    assert late_fee(22, 18, False) == 2000


def test_late_fee_just_over_cap():
    # 500 + 16*100 = 2100 -> capped to 2000
    assert late_fee(23, 18, False) == 2000


def test_late_fee_cap_with_surcharge():
    assert late_fee(30, 25, False) == 2000
