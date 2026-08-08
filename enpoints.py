HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive" # Better for session stability
}


VTOP_BASE_URL="https://vtop.vitap.ac.in/"
OPEN_PAGE="/vtop/open/page"
PRE_LOGIN="/vtop/prelogin/setup"

POST_PRE_LOGIN="/vtop/login"

OTP="/vtop/login/error"
VALIDATE_OTP="/vtop/validateSecurityOtp"

CONTENT="/vtop/content"

TIME_TABLE_PRE="/vtop/academics/common/StudentTimeTable"
PROCESS_TABLE="/vtop/processViewTimeTable"

ATTENDANCE_PRE="/vtop/academics/common/StudentAttendance"
PROCESS_ATTENDANCE="/vtop/processViewStudentAttendance"

OUTING="vtop/hostel/saveOutingForm"

STUDENT_DETAILS="vtop/studentsRecord/StudentProfileAllView"

EXAM_SCHEDULE="/vtop/examinations/doSearchExamScheduleForStudent"

BIOMETRIC_INFO="/vtop/getStudBioHistory"

MARKS_INFO="/vtop/examinations/doStudentMarkView"

GRADES_INFO="/vtop/examinations/examGradeView/doStudentGradeView"
GRADES_DETAILS="/vtop/examinations/examGradeView/getGradeViewDetails"
GRADE_HISTORY="/vtop/examinations/examGradeView/StudentGradeHistory"