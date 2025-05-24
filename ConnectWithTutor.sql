CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE "PaymentStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "ScheduleStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "StudentRequestStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "TutorApplicationStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "ClassStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "Role" (
  "roleId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "roleName" VARCHAR(20)
);

CREATE TABLE "User" (
  "userId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "username" VARCHAR(50) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "fullName" VARCHAR(50) NOT NULL,
  "birthDate" DATE,
  "phoneNumber" VARCHAR(20),
  "address" VARCHAR(50),
  "email" VARCHAR(50),
  "avatarUrl" TEXT,
  "averageRating" DECIMAL(3,2) DEFAULT 5,
  "roleId" UUID NOT NULL,
  "isVerified" BOOL DEFAULT 'False'
);

CREATE TABLE "StudentProfile" (
  "studentId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID NOT NULL,
  "gradeLevel" VARCHAR(20),
  "learningGoals" TEXT,
  "preferredStudyTime" TEXT,
  "description" VARCHAR(255)
);

CREATE TABLE "TutorProfile" (
  "tutorId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID NOT NULL,
  "degree" VARCHAR(100),
  "certificate" VARCHAR(100),
  "experience" VARCHAR(255),
  "description" VARCHAR(255),
  "introVideoUrl" TEXT,
  "isApproved" BOOL DEFAULT 'False'
);

CREATE TABLE "UserSocialAccount" (
  "socialAccountId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID NOT NULL,
  "provider" VARCHAR(20),
  "providerUserId" VARCHAR(100),
  "email" VARCHAR(100),
  "linkedAt" TIMESTAMPTZ
);

CREATE TABLE "Subject" (
  "subjectId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "subjectName_vi" VARCHAR(100),
  "subjectName_en" VARCHAR(100),
  "description" VARCHAR(255)
);

CREATE TABLE "StudentRequest" (
  "requestId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "studentId" UUID NOT NULL,
  "subjectId" UUID NOT NULL,
  "studyType" VARCHAR(20),
  "preferredSchedule" TEXT,
  "tuitionFee" DECIMAL(10,2),
  "location" VARCHAR(100),
  "description" TEXT,
  "status" UUID NOT NULL,
  "title" TEXT,
  "studentCount" INT DEFAULT 1,
  "createAt" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "TutorApplication" (
  "applicationId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "tutorId" UUID NOT NULL,
  "requestId" UUID NOT NULL,
  "applicationDate" TIMESTAMPTZ,
  "status" UUID NOT NULL
);

CREATE TABLE "Class" (
  "classId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "createdBy" UUID NOT NULL,  
  "className_vi" VARCHAR(100),
  "className_en" VARCHAR(100),
  "subjectId" UUID NOT NULL,
  "tutorId" UUID NOT NULL,
  "studyType" VARCHAR(20),
  "startDate" DATE,
  "sessions" INT,
  "tuitionFee" DECIMAL(10,2),
  "description" TEXT,
  "maxStudents" INT,
  "status" UUID NOT NULL
);

CREATE TABLE "ClassRegistration" (
  "registrationId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "classId" UUID NOT NULL,
  "studentId" UUID NOT NULL,
  "registrationDate" TIMESTAMPTZ
);

CREATE TABLE "Schedule" (
  "scheduleId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "classId" UUID NOT NULL,
  "zoomStartUrl" TEXT,
  "zoomUrl" TEXT,
  "zoomMeetingId" VARCHAR(50),
  "zoomPassword" VARCHAR(50),
  "zoomPublicId" VARCHAR(50),
  "dayStudying" DATE,
  "startTime" TIME,
  "endTime" TIME,
  "status" UUID NOT NULL
);

CREATE TABLE "PaymentMethod" (
  "methodId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "methodName" VARCHAR(50) NOT NULL,
  "description" TEXT,
  "isActive" BOOL,
  "logoUrl" TEXT,
  "logoPublicId" TEXT
);

CREATE TABLE "Payment" (
  "paymentId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "registrationId" UUID NOT NULL,
  "amount" DECIMAL(10,2),
  "paymentDate" TIMESTAMPTZ,
  "methodId" UUID NOT NULL,
  "status" UUID NOT NULL
);

CREATE TABLE "Evaluation" (
  "evaluationId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "classId" UUID NOT NULL,
  "fromUserId" UUID NOT NULL,
  "toUserId" UUID NOT NULL,
  "criteria1" INT,
  "criteria2" INT,
  "criteria3" INT,
  "comment" TEXT,
  "evaluationDate" TIMESTAMPTZ
);

CREATE TABLE "Notification" (
  "notificationId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "fromUserId" UUID NOT NULL,
  "toUserId" UUID NOT NULL,
  "title_vi" VARCHAR(100),
  "title_en" VARCHAR(100),
  "message_vi" TEXT,
  "message_en" TEXT,
  "type" VARCHAR(20),
  "isRead" BOOL,
  "createdAt" TIMESTAMPTZ
);

CREATE TABLE "Address" (
  "addressId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID,
  "classId" UUID,
  "requestId" UUID,
  "province" VARCHAR(50),
  "district" VARCHAR(50),
  "ward" VARCHAR(50),
  "street" VARCHAR(100),
  "fullAddress" VARCHAR(255),
  "latitude" DECIMAL(10,8),
  "longitude" DECIMAL(11,8)
);

CREATE TABLE "ComplaintType" (
  "complaintTypeId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" VARCHAR(100),
  "description" TEXT
);

CREATE TABLE "Complaint" (
  "complaintId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID,
  "complaintTypeId" UUID,
  "title" VARCHAR(100),
  "content" TEXT,
  "resolution_note" TEXT,
  "status" VARCHAR(50),
  "createdAt" TIMESTAMPTZ
);

CREATE TABLE "Conversation" (
  "conversationId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "type" VARCHAR(20),
  "createdAt" TIMESTAMPTZ
);

CREATE TABLE "ConversationParticipant" (
  "participantId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "conversationId" UUID NOT NULL,
  "userId" UUID NOT NULL,
  "joinedAt" TIMESTAMPTZ,
  "isMuted" BOOL DEFAULT false
);

CREATE TABLE "Message" (
  "messageId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "conversationId" UUID NOT NULL,
  "senderId" UUID NOT NULL,
  "content" TEXT,
  "messageType" VARCHAR(20),
  "sentAt" TIMESTAMPTZ,
  "isEdited" BOOL DEFAULT false,
  "isDeleted" BOOL DEFAULT false
);

CREATE TABLE "MessageFile" (
  "fileId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "messageId" UUID NOT NULL,
  "fileUrl" TEXT,
  "fileName" VARCHAR(255),
  "fileType" VARCHAR(50),
  "fileSize" INT
);

CREATE TABLE "MessageStatus" (
  "statusId" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "messageId" UUID NOT NULL,
  "userId" UUID NOT NULL,
  "isRead" BOOL DEFAULT false,
  "readAt" TIMESTAMPTZ
);

ALTER TABLE "User" ADD CONSTRAINT "FK_User_Role" FOREIGN KEY ("roleId") REFERENCES "Role" ("roleId");

ALTER TABLE "TutorProfile" ADD CONSTRAINT "FK_TutorProfile_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "StudentProfile" ADD CONSTRAINT "FK_StudentProfile_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "UserSocialAccount" ADD CONSTRAINT "FK_UserSocialAccount_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "StudentRequest" ADD CONSTRAINT "FK_StudentRequest_Student" FOREIGN KEY ("studentId") REFERENCES "User" ("userId");

ALTER TABLE "TutorApplication" ADD CONSTRAINT "FK_TutorApplication_Tutor" FOREIGN KEY ("tutorId") REFERENCES "User" ("userId");

ALTER TABLE "StudentRequest" ADD CONSTRAINT "FK_StudentRequest_Subject" FOREIGN KEY ("subjectId") REFERENCES "Subject" ("subjectId");

ALTER TABLE "TutorApplication" ADD CONSTRAINT "FK_TutorApplication_Request" FOREIGN KEY ("requestId") REFERENCES "StudentRequest" ("requestId");

ALTER TABLE "Class" ADD CONSTRAINT "FK_Class_Subject" FOREIGN KEY ("subjectId") REFERENCES "Subject" ("subjectId");

ALTER TABLE "Class" ADD CONSTRAINT "FK_Class_User" FOREIGN KEY ("createdBy") REFERENCES "User" ("userId");

ALTER TABLE "Class" ADD CONSTRAINT "FK_Class_Tutor" FOREIGN KEY ("tutorId") REFERENCES "User" ("userId");

ALTER TABLE "ClassRegistration" ADD CONSTRAINT "FK_ClassRegistration_Class" FOREIGN KEY ("classId") REFERENCES "Class" ("classId");

ALTER TABLE "ClassRegistration" ADD CONSTRAINT "FK_ClassRegistration_User" FOREIGN KEY ("studentId") REFERENCES "User" ("userId");

ALTER TABLE "Schedule" ADD CONSTRAINT "FK_Schedule_Class" FOREIGN KEY ("classId") REFERENCES "Class" ("classId");

ALTER TABLE "Payment" ADD CONSTRAINT "FK_Payment_Method" FOREIGN KEY ("methodId") REFERENCES "PaymentMethod" ("methodId");

ALTER TABLE "Payment" ADD CONSTRAINT "FK_Payment_ClassRegistration" FOREIGN KEY ("registrationId") REFERENCES "ClassRegistration" ("registrationId");

ALTER TABLE "Evaluation" ADD CONSTRAINT "FK_Evaluation_Class" FOREIGN KEY ("classId") REFERENCES "Class" ("classId");

ALTER TABLE "Evaluation" ADD CONSTRAINT "FK_Evaluation_FromUser" FOREIGN KEY ("fromUserId") REFERENCES "User" ("userId");

ALTER TABLE "Evaluation" ADD CONSTRAINT "FK_Evaluation_ToUser" FOREIGN KEY ("toUserId") REFERENCES "User" ("userId");

ALTER TABLE "Notification" ADD CONSTRAINT "FK_Notification_FromUser" FOREIGN KEY ("fromUserId") REFERENCES "User" ("userId");

ALTER TABLE "Notification" ADD CONSTRAINT "FK_Notification_ToUser" FOREIGN KEY ("toUserId") REFERENCES "User" ("userId");

ALTER TABLE "Address" ADD CONSTRAINT "FK_Address_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "Address" ADD CONSTRAINT "FK_Address_Class" FOREIGN KEY ("classId") REFERENCES "Class" ("classId");

ALTER TABLE "Address" ADD CONSTRAINT "FK_Address_Request" FOREIGN KEY ("requestId") REFERENCES "StudentRequest" ("requestId");

ALTER TABLE "ConversationParticipant" ADD CONSTRAINT "FK_ConversationParticipant_Conversation" FOREIGN KEY ("conversationId") REFERENCES "Conversation" ("conversationId");

ALTER TABLE "ConversationParticipant" ADD CONSTRAINT "FK_ConversationParticipant_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "Message" ADD CONSTRAINT "FK_Message_Conversation" FOREIGN KEY ("conversationId") REFERENCES "Conversation" ("conversationId");

ALTER TABLE "Message" ADD CONSTRAINT "FK_Message_Sender" FOREIGN KEY ("senderId") REFERENCES "User" ("userId");

ALTER TABLE "MessageFile" ADD CONSTRAINT "FK_MessageFile_Message" FOREIGN KEY ("messageId") REFERENCES "Message" ("messageId");

ALTER TABLE "MessageStatus" ADD CONSTRAINT "FK_MessageStatus_Message" FOREIGN KEY ("messageId") REFERENCES "Message" ("messageId");

ALTER TABLE "MessageStatus" ADD CONSTRAINT "FK_MessageStatus_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

ALTER TABLE "StudentRequest" ADD CONSTRAINT "FK_StudentRequest_Status" FOREIGN KEY ("status") REFERENCES "StudentRequestStatus" ("statusId");

ALTER TABLE "TutorApplication" ADD CONSTRAINT "FK_TutorApplication_Status" FOREIGN KEY ("status") REFERENCES "TutorApplicationStatus" ("statusId");

ALTER TABLE "Class" ADD CONSTRAINT "FK_Class_Status" FOREIGN KEY ("status") REFERENCES "ClassStatus" ("statusId");

ALTER TABLE "Schedule" ADD CONSTRAINT "FK_Schedule_Status" FOREIGN KEY ("status") REFERENCES "ScheduleStatus" ("statusId");

ALTER TABLE "Payment" ADD CONSTRAINT "FK_Payment_Status" FOREIGN KEY ("status") REFERENCES "PaymentStatus" ("statusId");

ALTER TABLE "Complaint" ADD CONSTRAINT "FK_Complaint_ComplaintType" FOREIGN KEY ("complaintTypeId") REFERENCES "ComplaintType" ("complaintTypeId");

ALTER TABLE "Complaint" ADD CONSTRAINT "FK_Complaint_User" FOREIGN KEY ("userId") REFERENCES "User" ("userId");

-- Chèn dữ liệu mặc định cho PaymentStatus
INSERT INTO "PaymentStatus" ("code", "name")
VALUES
  ('Unpaid', 'Chưa thanh toán'),
  ('Pending', 'Đang xử lý'),
  ('Success', 'Đã hoàn thành');

-- Chèn dữ liệu mặc định cho ScheduleStatus
INSERT INTO "ScheduleStatus" ("code", "name")
VALUES
  ('scheduled', 'Buổi học đã được lên lịch, chờ đến thời gian bắt đầu'),
  ('Ongoing', 'Buổi học đang diễn ra'),
  ('Completed', 'Buổi học đã kết thúc'),
  ('Cancelled', 'Buổi học đã bị hủy/tạm ngưng');

-- Chèn dữ liệu mặc định cho StudentRequestStatus
INSERT INTO "StudentRequestStatus" ("code", "name")
VALUES
  ('Pending', 'Yêu cầu mới được tạo, đang chờ gia sư ứng tuyển'),
  ('InProgress', 'Đã chọn gia sư và đang chuẩn bị tiến hành mở lớp'),
  ('Completed', 'Đã hoàn thành yêu cầu tìm gia sư'),
  ('Cancelled', 'Yêu cầu bị học viên hủy hoặc hết hiệu lực');

-- Chèn dữ liệu mặc định cho TutorApplicationStatus
INSERT INTO "TutorApplicationStatus" ("code", "name")
VALUES
  ('Pending', 'Gia sư đã ứng tuyển, đang chờ học viên xem xét/chấp nhận'),
  ('Accepted', 'Học viên đã chấp nhận gia sư'),
  ('Rejected', 'Học viên từ chối hồ sơ ứng tuyển'),
  ('Withdrawn', 'Gia sư rút lại đơn ứng tuyển trước khi được học viên xử lý'),
  ('Cancelled', 'Bị hủy bởi hệ thống, admin, hoặc do yêu cầu học tập không còn hiệu lực nữa'),
  ('Completed', 'Yêu cầu đã được xử lý xong');

-- Chèn dữ liệu mặc định cho ClassStatus
INSERT INTO "ClassStatus" ("code", "name")
VALUES
  ('Pending', 'Chờ duyệt lớp'),
  ('Open', 'Lớp học đang mở để học viên đăng ký'),
  ('Full', 'Lớp học đã đủ số lượng học viên'),
  ('Cancelled', 'Hủy lớp vì 1 số lý do nào đó');

-- Chèn dữ liệu mặc định cho ComplaintType
INSERT INTO "ComplaintType" ("name", "description")
VALUES
  ('Lịch học', 'Vấn đề liên quan đến thời gian, lịch học bị thay đổi hoặc hủy mà không báo trước'),
  ('Thanh toán', 'Khiếu nại liên quan đến việc thanh toán học phí, hoàn tiền, hoặc hóa đơn không chính xác'),
  ('Chất lượng giảng dạy', 'Gia sư không đảm bảo chất lượng hoặc không đúng như mô tả ban đầu'),
  ('Kỹ thuật/Zoom', 'Vấn đề kỹ thuật khi tham gia học online như link Zoom không hoạt động hoặc âm thanh kém'),
  ('Hủy lớp', 'Khiếu nại về việc lớp học bị hủy mà không có lý do rõ ràng hoặc không được hoàn tiền'),
  ('Thông báo/Thông tin sai lệch', 'Thông tin mô tả lớp, yêu cầu, lịch học không chính xác'),
  ('Khác', 'Các vấn đề khác không thuộc các loại trên');
