CREATE TABLE "PaymentStatus" (
  "statusId" VARCHAR(10) PRIMARY KEY,
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "ScheduleStatus" (
  "statusId" VARCHAR(10) PRIMARY KEY,
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "StudentRequestStatus" (
  "statusId" VARCHAR(10) PRIMARY KEY,
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "TutorApplicationStatus" (
  "statusId" VARCHAR(10) PRIMARY KEY,
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "ClassStatus" (
  "statusId" VARCHAR(10) PRIMARY KEY,
  "code" VARCHAR(20) UNIQUE NOT NULL,
  "name" VARCHAR(100) NOT NULL
);

CREATE TABLE "Role" (
  "roleId" VARCHAR(10) PRIMARY KEY,
  "roleName" VARCHAR(20)
);

CREATE TABLE "User" (
  "userId" VARCHAR(50) PRIMARY KEY,
  "username" VARCHAR(50) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "fullName" VARCHAR(50) NOT NULL,
  "birthDate" DATE,
  "phoneNumber" VARCHAR(20),
  "address" VARCHAR(50),
  "email" VARCHAR(50),
  "avatarUrl" TEXT,
  "averageRating" DECIMAL(3,2) DEFAULT 5,
  "roleId" VARCHAR(10) NOT NULL,
  "isVerified" BOOL DEFAULT 'False'
);

CREATE TABLE "StudentProfile" (
  "studentId" VARCHAR(50) PRIMARY KEY,
  "userId" VARCHAR(50) NOT NULL,
  "gradeLevel" VARCHAR(20),
  "learningGoals" TEXT,
  "preferredStudyTime" TEXT,
  "description" VARCHAR(255)
);

CREATE TABLE "TutorProfile" (
  "tutorId" VARCHAR(50) PRIMARY KEY,
  "userId" VARCHAR(50) NOT NULL,
  "degree" VARCHAR(100),
  "certificate" VARCHAR(100),
  "experience" VARCHAR(255),
  "description" VARCHAR(255),
  "introVideoUrl" TEXT,
  "isApproved" BOOL DEFAULT 'False'
);

CREATE TABLE "UserSocialAccount" (
  "socialAccountId" VARCHAR(50) PRIMARY KEY,
  "userId" VARCHAR(50) NOT NULL,
  "provider" VARCHAR(20),
  "providerUserId" VARCHAR(100),
  "email" VARCHAR(100),
  "linkedAt" TIMESTAMP
);

CREATE TABLE "Subject" (
  "subjectId" VARCHAR(50) PRIMARY KEY,
  "subjectName_vi" VARCHAR(100),
  "subjectName_en" VARCHAR(100),
  "description" VARCHAR(255)
);

CREATE TABLE "StudentRequest" (
  "requestId" VARCHAR(50) PRIMARY KEY,
  "studentId" VARCHAR(50) NOT NULL,
  "subjectId" VARCHAR(50) NOT NULL,
  "studyType" VARCHAR(20),
  "preferredSchedule" TEXT,
  "tuitionFee" DECIMAL(10,2),
  "location" VARCHAR(100),
  "description" TEXT,
  "status" VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE "TutorApplication" (
  "applicationId" VARCHAR(50) PRIMARY KEY,
  "tutorId" VARCHAR(50) NOT NULL,
  "requestId" VARCHAR(50) NOT NULL,
  "applicationDate" TIMESTAMP,
  "status" VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE "Class" (
  "classId" VARCHAR(50) PRIMARY KEY,
  "createdBy" VARCHAR(50) NOT NULL,  
  "className_vi" VARCHAR(100),
  "className_en" VARCHAR(100),
  "subjectId" VARCHAR(50) NOT NULL,
  "tutorId" VARCHAR(50) NOT NULL,
  "studyType" VARCHAR(20),
  "startDate" DATE,
  "sessions" INT,
  "tuitionFee" DECIMAL(10,2),
  "description" TEXT,
  "maxStudents" INT,
  "status" VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE "ClassRegistration" (
  "registrationId" VARCHAR(50) PRIMARY KEY,
  "classId" VARCHAR(50) NOT NULL,
  "studentId" VARCHAR(50) NOT NULL,
  "registrationDate" TIMESTAMP
);

CREATE TABLE "Schedule" (
  "scheduleId" VARCHAR(50) PRIMARY KEY,
  "classId" VARCHAR(50) NOT NULL,
  "zoomUrl" TEXT,
  "zoomMeetingId" VARCHAR(50),
  "zoomPassword" VARCHAR(50),
  "date" DATE,
  "startTime" TIME,
  "endTime" TIME,
  "status" VARCHAR(20) NOT NULL DEFAULT 'Scheduled'
);

CREATE TABLE "PaymentMethod" (
  "methodId" VARCHAR(20) PRIMARY KEY,
  "methodName" VARCHAR(50) NOT NULL,
  "description" TEXT,
  "isActive" BOOL,
  "logoUrl" TEXT
);

CREATE TABLE "Payment" (
  "paymentId" VARCHAR(50) PRIMARY KEY,
  "registrationId" VARCHAR(50) NOT NULL,
  "amount" DECIMAL(10,2),
  "paymentDate" TIMESTAMP,
  "methodId" VARCHAR(20) NOT NULL,
  "status" VARCHAR(10) NOT NULL DEFAULT 'Unpaid'
);

CREATE TABLE "Evaluation" (
  "evaluationId" VARCHAR(50) PRIMARY KEY,
  "classId" VARCHAR(50) NOT NULL,
  "fromUserId" VARCHAR(50) NOT NULL,
  "toUserId" VARCHAR(50) NOT NULL,
  "criteria1" INT,
  "criteria2" INT,
  "criteria3" INT,
  "comment" TEXT,
  "evaluationDate" TIMESTAMP
);

CREATE TABLE "Notification" (
  "notificationId" VARCHAR(50) PRIMARY KEY,
  "fromUserId" VARCHAR(50) NOT NULL,
  "toUserId" VARCHAR(50) NOT NULL,
  "title_vi" VARCHAR(100),
  "title_en" VARCHAR(100),
  "message_vi" TEXT,
  "message_en" TEXT,
  "type" VARCHAR(20),
  "isRead" BOOL,
  "createdAt" TIMESTAMP
);

CREATE TABLE "Address" (
  "addressId" VARCHAR(50) PRIMARY KEY,
  "userId" VARCHAR(50),
  "classId" VARCHAR(50),
  "requestId" VARCHAR(50),
  "province" VARCHAR(50),
  "district" VARCHAR(50),
  "ward" VARCHAR(50),
  "street" VARCHAR(100),
  "fullAddress" VARCHAR(255),
  "latitude" DECIMAL(10,8),
  "longitude" DECIMAL(11,8)
);

CREATE TABLE "Conversation" (
  "conversationId" VARCHAR(50) PRIMARY KEY,
  "type" VARCHAR(20),
  "createdAt" TIMESTAMP
);

CREATE TABLE "ConversationParticipant" (
  "participantId" VARCHAR(50) PRIMARY KEY,
  "conversationId" VARCHAR(50) NOT NULL,
  "userId" VARCHAR(50) NOT NULL,
  "joinedAt" TIMESTAMP,
  "isMuted" BOOL DEFAULT false
);

CREATE TABLE "Message" (
  "messageId" VARCHAR(50) PRIMARY KEY,
  "conversationId" VARCHAR(50) NOT NULL,
  "senderId" VARCHAR(50) NOT NULL,
  "content" TEXT,
  "messageType" VARCHAR(20),
  "sentAt" TIMESTAMP,
  "isEdited" BOOL DEFAULT false,
  "isDeleted" BOOL DEFAULT false
);

CREATE TABLE "MessageFile" (
  "fileId" VARCHAR(50) PRIMARY KEY,
  "messageId" VARCHAR(50) NOT NULL,
  "fileUrl" TEXT,
  "fileName" VARCHAR(255),
  "fileType" VARCHAR(50),
  "fileSize" INT
);

CREATE TABLE "MessageStatus" (
  "statusId" VARCHAR(50) PRIMARY KEY,
  "messageId" VARCHAR(50) NOT NULL,
  "userId" VARCHAR(50) NOT NULL,
  "isRead" BOOL DEFAULT false,
  "readAt" TIMESTAMP
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
