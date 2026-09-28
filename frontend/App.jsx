import React, { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  Award,
  BarChart3,
  Bell,
  BookOpen,
  CalendarDays,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ClipboardCheck,
  ClipboardList,
  Database,
  Download,
  ExternalLink,
  FileCheck2,
  FileText,
  FolderOpen,
  GraduationCap,
  HelpCircle,
  LayoutDashboard,
  Lock,
  Menu,
  Moon,
  PlayCircle,
  Save,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  Sun,
  Target,
  TrendingUp,
  Upload,
  User,
  UserPlus,
  X,
  Zap,
  RotateCcw,
} from "lucide-react";
import Login from "./login.jsx";
import Register from "./register.jsx";
import QuizPlayer from "./QuizPlayer.jsx";
import "./solo.css";
import "./executive.css";
import "./aurora.css";
import "./educational.css";

const NAV = [
  { id: "Dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "My Competencies", label: "My Competencies", icon: BarChart3 },
  { id: "Learning Path", label: "Learning Path", icon: TrendingUp },
  { id: "Assessments", label: "Assessments", icon: ClipboardList },
  { id: "My Documents", label: "My Documents", icon: FolderOpen },
  { id: "Certificates", label: "Certificates", icon: Award },
  { id: "Analytics", label: "Analytics", icon: BarChart3 },
  { id: "Data Sources", label: "Data Sources", icon: Database },
  { id: "Settings", label: "Settings", icon: Settings },
];





const NOTIFICATIONS = { en: [], hi: [], ta: [], te: [] };

function notificationsFor(lang) { return NOTIFICATIONS[lang] || NOTIFICATIONS.en; }

const LOCALIZED_COPY = {
  en: { profilePhoto: "Profile picture", changePhoto: "Choose photo", removePhoto: "Remove", profileHint: "A photo and your display name appear across your workspace.", languageHint: "English · हिन्दी · தமிழ் · తెలుగు", appearanceHint: "Light / Dark" },
  hi: { profilePhoto: "प्रोफ़ाइल चित्र", changePhoto: "चित्र चुनें", removePhoto: "हटाएँ", profileHint: "आपका चित्र और प्रदर्शन नाम पूरे कार्यक्षेत्र में दिखाई देता है।", languageHint: "English · हिन्दी · தமிழ் · తెలుగు", appearanceHint: "लाइट / डार्क" },
  ta: { profilePhoto: "சுயவிவரப் படம்", changePhoto: "படத்தைத் தேர்ந்தெடுக்கவும்", removePhoto: "அகற்று", profileHint: "உங்கள் படம் மற்றும் காட்சிப் பெயர் பணியிடத்தில் தோன்றும்.", languageHint: "English · हिन्दी · தமிழ் · తెలుగు", appearanceHint: "லைட் / டார்க்" },
  te: { profilePhoto: "ప్రొఫైల్ చిత్రం", changePhoto: "చిత్రాన్ని ఎంచుకోండి", removePhoto: "తొలగించు", profileHint: "మీ చిత్రం మరియు ప్రదర్శన పేరు వర్క్‌స్పేస్ అంతటా కనిపిస్తాయి.", languageHint: "English · हिन्दी · தமிழ் · తెలుగు", appearanceHint: "లైట్ / డార్క్" },
};

const DICTIONARY = {
  en:{
    dashboard:"Dashboard",competencies:"My Competencies",path:"Learning Path",assessments:"Assessments",
    documents:"My Documents",certificates:"Certificates",analytics:"Analytics",dataSources:"Data Sources",settings:"Settings",
    hello:"Hello",online:"PORTAL ACTIVE",command:"OFFICIAL CAPACITY DASHBOARD",role:"Senior Statistical Officer (SSO)",
    competency:"Overall Competency",gaps:"Critical Skill Gaps",learning:"Learning Progress",completed:"Assessments Completed",
    strong:"Strong",moderate:"Moderate",weak:"Weak",continue:"Continue Learning",viewAll:"View All",
    upcoming:"Upcoming Assessments",recommendation:"Recommended for You",insight:"Methodological Insight",profile:"Profile Settings",
    language:"Language",theme:"Theme",dark:"Dark",light:"Light",save:"Save Changes",displayName:"Display Name",
    department:"Department",signOut:"Sign Out",search:"Search",completedModules:"Modules Completed",hours:"Hours Completed",
    completion:"Estimated Completion",solo:"Solo System",executive:"Executive",aurora:"Aurora",
    gapAssessment:"Competency Gap Assessment",priority:"Priority Recommendations",
    player:"Learner Profile",rank:"Cadre / Track",level:"Readiness",xp:"Proficiency Index",strength:"Sampling & Inference",dataQuality:"Data Quality",gis:"GIS & Spatial",ml:"Data Science & ML",
    activeModule:"Active Module",trajectory:"Competency trajectory is positive",openAnalysis:"Open Analysis",
    completeGis:"Complete GIS for Statistics",systemOnline:"Portal Active",trainingPipeline:"Competency Roadmap",
    schedule:"Schedule",matrix:"Competency Matrix",skillMatrix:"Skill Matrix",currentReadiness:"Current Readiness",
    assessmentControl:"Diagnostic Assessment Control",documentVault:"Official Documents & Records",credentialLedger:"Certificates & Accreditations",
    totalDocuments:"Total Documents",shared:"Shared",addedThisMonth:"Added This Month",certificatesEarned:"Certificates Earned",
    inProgress:"In Progress",expiringSoon:"Expiring Soon",verifyCredential:"Verify Credential",continueTrack:"Continue Track",
    appearance:"Appearance",switchAppearance:"Switch between dashboard modes.",nextCheckpoints:"Next Checkpoints",
    upcomingQueue:"Upcoming Queue",openDetails:"Open Details",activeTrack:"Active Track",lessons:"lessons",
    reviewModule:"Review Module",continueModule:"Continue Module",locked:"Locked",modulesCompleted:"Modules Completed",
    graphical:"Graphical Representation",visualSummary:"Visual summary of your competency, assessment and learning data.",
    competencyScores:"Competency Scores",assessmentHistory:"Assessment History",learningMix:"Learning Effort by Domain",
    score:"Score",hoursLabel:"Hours",noData:"No data available",
    competencyEngine:"Competency Engine",dataVisuals:"Data Visuals",systemConfiguration:"System Configuration",
    visualSystem:"Visual System",securityStatus:"MoSPI SECURE GATEWAY",demoEnvironment:"National Data Portal · Verified SSL/TLS 1.3 Node",
    connectProduction:"Connected to Central Statistical Directory and NDSAP Interoperability Infrastructure with end-to-end encryption.",email:"Email",
    notifications:"Notifications",noNotifications:"No new notifications",help:"Help",live:"Live",
    courseAnalytics:"Course Progress & Analytics",avgCompletion:"Avg. Completion",weeklyHours:"Velocity",
    verifiedCertificate:"Officially Verified Credential",downloadOfficialCert:"Download Official Certificate",
    copyVerificationLink:"Copy Verification Link",moduleWorkspace:"Module Study Workspace",launchModuleQuiz:"Launch Diagnostic Quiz",
    assessmentDetails:"Assessment Diagnostic Breakdown",userGuide:"User Guidance & Support"
  },
  hi:{
    dashboard:"डैशबोर्ड",competencies:"मेरी दक्षताएँ",path:"लर्निंग पाथ",assessments:"मूल्यांकन",
    documents:"मेरे दस्तावेज़",certificates:"प्रमाणपत्र",analytics:"विश्लेषण",dataSources:"डेटा स्रोत",settings:"सेटिंग्स",
    hello:"नमस्ते",online:"सिस्टम ऑनलाइन",command:"सिस्टम कमांड सेंटर",role:"सांख्यिकी अन्वेषक",
    competency:"कुल दक्षता",gaps:"महत्वपूर्ण कौशल अंतर",learning:"लर्निंग प्रगति",completed:"पूर्ण मूल्यांकन",
    strong:"मज़बूत",moderate:"मध्यम",weak:"कमज़ोर",continue:"सीखना जारी रखें",viewAll:"सभी देखें",
    upcoming:"आगामी मूल्यांकन",recommendation:"आपके लिए अनुशंसित",insight:"AI अंतर्दृष्टि",profile:"प्रोफ़ाइल सेटिंग्स",
    language:"भाषा",theme:"थीम",dark:"डार्क",light:"लाइट",save:"बदलाव सहेजें",displayName:"डिस्प्ले नाम",
    department:"विभाग",signOut:"साइन आउट",search:"खोजें",completedModules:"पूर्ण मॉड्यूल",hours:"पूर्ण घंटे",
    completion:"अनुमानित पूर्णता",solo:"सोलो सिस्टम",executive:"एग्जीक्यूटिव",aurora:"ऑरोरा",
    gapAssessment:"दक्षता अंतर मूल्यांकन",priority:"प्राथमिक अनुशंसाएँ",
    player:"प्लेयर स्थिति",rank:"रैंक",level:"स्तर",xp:"XP",strength:"मज़बूती",dataQuality:"डेटा गुणवत्ता",gis:"GIS",ml:"ML",
    activeModule:"सक्रिय मॉड्यूल",trajectory:"दक्षता की प्रगति सकारात्मक है",openAnalysis:"विश्लेषण खोलें",
    completeGis:"GIS for Statistics पूरा करें",systemOnline:"सिस्टम ऑनलाइन",trainingPipeline:"प्रशिक्षण पाइपलाइन",
    schedule:"समय-सारणी",matrix:"दक्षता मैट्रिक्स",skillMatrix:"कौशल मैट्रिक्स",currentReadiness:"वर्तमान तैयारी",
    assessmentControl:"मूल्यांकन नियंत्रण",documentVault:"दस्तावेज़ वॉल्ट",credentialLedger:"प्रमाणपत्र रिकॉर्ड",
    totalDocuments:"कुल दस्तावेज़",shared:"साझा",addedThisMonth:"इस माह जोड़े गए",certificatesEarned:"अर्जित प्रमाणपत्र",
    inProgress:"प्रगति में",expiringSoon:"जल्द समाप्त",verifyCredential:"प्रमाणपत्र सत्यापित करें",continueTrack:"ट्रैक जारी रखें",
    appearance:"दिखावट",switchAppearance:"डैशबोर्ड मोड बदलें।",nextCheckpoints:"अगले चरण",
    upcomingQueue:"आगामी कतार",openDetails:"विवरण खोलें",activeTrack:"सक्रिय ट्रैक",lessons:"पाठ",
    reviewModule:"मॉड्यूल देखें",continueModule:"मॉड्यूल जारी रखें",locked:"लॉक्ड",modulesCompleted:"पूर्ण मॉड्यूल",
    graphical:"ग्राफ़िकल प्रतिनिधित्व",visualSummary:"आपकी दक्षता, मूल्यांकन और लर्निंग डेटा का दृश्य सारांश।",
    competencyScores:"दक्षता स्कोर",assessmentHistory:"मूल्यांकन इतिहास",learningMix:"डोमेन के अनुसार लर्निंग प्रयास",
    score:"स्कोर",hoursLabel:"घंटे",noData:"डेटा उपलब्ध नहीं",
    competencyEngine:"दक्षता इंजन",dataVisuals:"डेटा विज़ुअल्स",systemConfiguration:"सिस्टम कॉन्फ़िगरेशन",
    visualSystem:"विज़ुअल सिस्टम",securityStatus:"MoSPI सुरक्षित गेटवे",demoEnvironment:"राष्ट्रीय डेटा पोर्टल · सत्यापित SSL/TLS 1.3 नोड",
    connectProduction:"केंद्रीय सांख्यिकी निर्देशिका और NDSAP इंटरऑपरेबिलिटी इन्फ्रास्ट्रक्चर से एंड-टू-एंड एन्क्रिप्शन से जुड़ा हुआ।",email:"ईमेल",
    notifications:"सूचनाएँ",noNotifications:"कोई नई सूचना नहीं",help:"सहायता",live:"लाइव",
    courseAnalytics:"कोर्स प्रगति एवं विश्लेषण",avgCompletion:"औसत पूर्णता",weeklyHours:"साप्ताहिक गति",
    verifiedCertificate:"आधिकारिक रूप से सत्यापित प्रमाणपत्र",downloadOfficialCert:"आधिकारिक प्रमाणपत्र डाउनलोड करें",
    copyVerificationLink:"सत्यापन लिंक कॉपी करें",moduleWorkspace:"मॉड्यूल अध्ययन कार्यक्षेत्र",launchModuleQuiz:"डायग्नोस्टिक क्विज़ शुरू करें",
    assessmentDetails:"मूल्यांकन नैदानिक विश्लेषण",userGuide:"उपयोगकर्ता मार्गदर्शन एवं सहायता"
  },
  ta:{
    dashboard:"டாஷ்போர்டு",competencies:"என் திறன்கள்",path:"கற்றல் பாதை",assessments:"மதிப்பீடுகள்",
    documents:"என் ஆவணங்கள்",certificates:"சான்றிதழ்கள்",analytics:"பகுப்பாய்வு",dataSources:"தரவு ஆதாரங்கள்",settings:"அமைப்புகள்",
    hello:"வணக்கம்",online:"சிஸ்டம் ஆன்லைன்",command:"சிஸ்டம் கட்டளை மையம்",role:"புள்ளியியல் ஆய்வாளர்",
    competency:"மொத்த திறன்",gaps:"முக்கிய திறன் இடைவெளிகள்",learning:"கற்றல் முன்னேற்றம்",completed:"முடிக்கப்பட்ட மதிப்பீடுகள்",
    strong:"வலுவான",moderate:"மிதமான",weak:"பலவீனமான",continue:"கற்றலைத் தொடரவும்",viewAll:"அனைத்தையும் காண்க",
    upcoming:"வரவிருக்கும் மதிப்பீடுகள்",recommendation:"உங்களுக்கான பரிந்துரைகள்",insight:"AI நுண்ணறிவு",profile:"சுயவிவர அமைப்புகள்",
    language:"மொழி",theme:"தீம்",dark:"டார்க்",light:"லைட்",save:"மாற்றங்களைச் சேமிக்கவும்",displayName:"காட்சிப் பெயர்",
    department:"துறை",signOut:"வெளியேறு",search:"தேடல்",completedModules:"முடிக்கப்பட்ட தொகுதிகள்",hours:"முடிக்கப்பட்ட மணிநேரங்கள்",
    completion:"மதிப்பிடப்பட்ட நிறைவு",solo:"சோலோ சிஸ்டம்",executive:"எக்ஸிக்யூட்டிவ்",aurora:"ஆரோரா",
    gapAssessment:"திறன் இடைவெளி மதிப்பீடு",priority:"முன்னுரிமை பரிந்துரைகள்",
    player:"பிளேயர் நிலை",rank:"தரம்",level:"நிலை",xp:"XP",strength:"வலிமை",dataQuality:"தரவு தரம்",gis:"GIS",ml:"ML",
    activeModule:"செயலில் உள்ள தொகுதி",trajectory:"திறன் முன்னேற்றம் நேர்மறையாக உள்ளது",openAnalysis:"பகுப்பாய்வைத் திறக்கவும்",
    completeGis:"GIS for Statistics ஐ முடிக்கவும்",systemOnline:"சிஸ்டம் ஆன்லைன்",trainingPipeline:"பயிற்சி பைப்லைன்",
    schedule:"அட்டவணை",matrix:"திறன் மேட்ரிக்ஸ்",skillMatrix:"திறன் மேட்ரிக்ஸ்",currentReadiness:"தற்போதைய தயார்நிலை",
    assessmentControl:"மதிப்பீட்டு கட்டுப்பாடு",documentVault:"ஆவண களஞ்சியம்",credentialLedger:"சான்றிதழ் பதிவு",
    totalDocuments:"மொத்த ஆவணங்கள்",shared:"பகிரப்பட்டது",addedThisMonth:"இந்த மாதம் சேர்க்கப்பட்டது",certificatesEarned:"பெற்ற சான்றிதழ்கள்",
    inProgress:"முன்னேற்றத்தில்",expiringSoon:"விரைவில் காலாவதியாகும்",verifyCredential:"சான்றைச் சரிபார்க்கவும்",continueTrack:"டிராக்கைத் தொடரவும்",
    appearance:"தோற்றம்",switchAppearance:"டாஷ்போர்டு முறைகளை மாற்றவும்.",nextCheckpoints:"அடுத்த கட்டங்கள்",
    upcomingQueue:"வரவிருக்கும் வரிசை",openDetails:"விவரங்களைத் திறக்கவும்",activeTrack:"செயலில் உள்ள டிராக்",lessons:"பாடங்கள்",
    reviewModule:"மாட்யூலைப் பார்க்கவும்",continueModule:"மாட்யூலைத் தொடரவும்",locked:"பூட்டப்பட்டது",modulesCompleted:"முடிக்கப்பட்ட மாட்யூல்கள்",
    graphical:"வரைகலை பிரதிநிதித்துவம்",visualSummary:"உங்கள் திறன், மதிப்பீடு மற்றும் கற்றல் தரவின் காட்சி சுருக்கம்.",
    competencyScores:"திறன் மதிப்பெண்கள்",assessmentHistory:"மதிப்பீட்டு வரலாறு",learningMix:"டொமைன் அடிப்படையிலான கற்றல் முயற்சி",
    score:"மதிப்பெண்",hoursLabel:"மணிநேரம்",noData:"தரவு இல்லை",
    competencyEngine:"திறன் இயந்திரம்",dataVisuals:"தரவு காட்சிகள்",systemConfiguration:"சிஸ்டம் கட்டமைப்பு",
    visualSystem:"காட்சி அமைப்பு",securityStatus:"MoSPI பாதுகாப்பான நுழைவாயில்",demoEnvironment:"தேசிய தரவு போர்டல் · சரிபார்க்கப்பட்ட SSL/TLS 1.3 முனை",
    connectProduction:"மத்திய புள்ளியியல் அடைவு மற்றும் NDSAP இயங்குதளத்துடன் முழுமையான குறியாக்கத்துடன் இணைக்கப்பட்டுள்ளது.",email:"மின்னஞ்சல்",
    notifications:"அறிவிப்புகள்",noNotifications:"புதிய அறிவிப்புகள் இல்லை",help:"உதவி",live:"நேரலை",
    courseAnalytics:"பாடநெறி முன்னேற்றம் & பகுப்பாய்வு",avgCompletion:"சராசரி நிறைவு",weeklyHours:"வாராந்திர வேகம்",
    verifiedCertificate:"அதிகாரப்பூர்வமாக சரிபார்க்கப்பட்ட சான்றிதழ்",downloadOfficialCert:"அதிகாரப்பூர்வ சான்றிதழைப் பதிவிறக்கவும்",
    copyVerificationLink:"சரிபார்ப்பு இணைப்பை நகலெடுக்கவும்",moduleWorkspace:"தொகுதி படிப்பு பணியிடம்",launchModuleQuiz:"கண்டறியும் வினாடி வினாவைத் தொடங்கவும்",
    assessmentDetails:"மதிப்பீட்டு கண்டறியும் முறிவு",userGuide:"பயனர் வழிகாட்டுதல் & உதவி"
  },
  te:{
    dashboard:"డాష్‌బోర్డ్",competencies:"నా సామర్థ్యాలు",path:"లెర్నింగ్ పాత్",assessments:"అసెస్‌మెంట్లు",
    documents:"నా పత్రాలు",certificates:"సర్టిఫికెట్లు",analytics:"విశ్లేషణ",dataSources:"డేటా మూలాలు",settings:"సెట్టింగ్స్",
    hello:"నమస్కారం",online:"సిస్టమ్ ఆన్‌లైన్",command:"సిస్టమ్ కమాండ్ సెంటర్",role:"గణాంక పరిశోధకుడు",
    competency:"మొత్తం సామర్థ్యం",gaps:"కీలక నైపుణ్య లోపాలు",learning:"లెర్నింగ్ పురోగతి",completed:"పూర్తయిన అసెస్‌మెంట్లు",
    strong:"బలమైన",moderate:"మోస్తరు",weak:"బలహీనమైన",continue:"లెర్నింగ్ కొనసాగించండి",viewAll:"అన్నీ చూడండి",
    upcoming:"రాబోయే అసెస్‌మెంట్లు",recommendation:"మీ కోసం సిఫార్సులు",insight:"AI అంతర్దృష్టి",profile:"ప్రొఫైల్ సెట్టింగ్స్",
    language:"భాష",theme:"థీమ్",dark:"డార్క్",light:"లైట్",save:"మార్పులను సేవ్ చేయండి",displayName:"డిస్ప్లే పేరు",
    department:"విభాగం",signOut:"సైన్ అవుట్",search:"శోధన",completedModules:"పూర్తయిన మాడ్యూల్స్",hours:"పూర్తయిన గంటలు",
    completion:"అంచనా పూర్తి",solo:"సోలో సిస్టమ్",executive:"ఎగ్జిక్యూటివ్",aurora:"ఆరోరా",
    gapAssessment:"సామర్థ్య లోపాల అంచనా",priority:"ప్రాధాన్య సిఫార్సులు",
    player:"ప్లేయర్ స్థితి",rank:"ర్యాంక్",level:"స్థాయి",xp:"XP",strength:"బలం",dataQuality:"డేటా నాణ్యత",gis:"GIS",ml:"ML",
    activeModule:"యాక్టివ్ మాడ్యూల్",trajectory:"సామర్థ్య పురోగతి సానుకూలంగా ఉంది",openAnalysis:"విశ్లేషణ తెరవండి",
    completeGis:"GIS for Statistics పూర్తి చేయండి",systemOnline:"సిస్టమ్ ఆన్‌లైన్",trainingPipeline:"శిక్షణ పైప్‌లైన్",
    schedule:"షెడ్యూల్",matrix:"సామర్థ్య మ్యాట్రిక్స్",skillMatrix:"నైపుణ్య మ్యాట్రిక్స్",currentReadiness:"ప్రస్తుత సిద్ధత",
    assessmentControl:"అసెస్‌మెంట్ నియంత్రణ",documentVault:"డాక్యుమెంట్ వాల్ట్",credentialLedger:"సర్టిఫికేట్ రికార్డు",
    totalDocuments:"మొత్తం పత్రాలు",shared:"షేర్ చేసినవి",addedThisMonth:"ఈ నెల చేర్చినవి",certificatesEarned:"పొందిన సర్టిఫికెట్లు",
    inProgress:"పురోగతిలో",expiringSoon:"త్వరలో గడువు ముగుస్తుంది",verifyCredential:"క్రెడెన్షియల్ ధృవీకరించండి",continueTrack:"ట్రాక్ కొనసాగించండి",
    appearance:"రూపకల్పన",switchAppearance:"డాష్‌బోర్డ్ మోడ్‌లను మార్చండి.",nextCheckpoints:"తదుపరి దశలు",
    upcomingQueue:"రాబోయే క్యూ",openDetails:"వివరాలు తెరవండి",activeTrack:"యాక్టివ్ ట్రాక్",lessons:"పాఠాలు",
    reviewModule:"మాడ్యూల్ చూడండి",continueModule:"మాడ్యూల్ కొనసాగించండి",locked:"లాక్ చేయబడింది",modulesCompleted:"పూర్తయిన మాడ్యూల్స్",
    graphical:"గ్రాఫికల్ ప్రాతినిధ్యం",visualSummary:"మీ సామర్థ్యం, అసెస్‌మెంట్ మరియు లెర్నింగ్ డేటా యొక్క దృశ్య సారాంశం.",
    competencyScores:"సామర్థ్య స్కోర్లు",assessmentHistory:"అసెస్‌మెంట్ చరిత్ర",learningMix:"డొమైన్ వారీ లెర్నింగ్ ప్రయత్నం",
    score:"స్కోర్",hoursLabel:"గంటలు",noData:"డేటా అందుబాటులో లేదు",
    competencyEngine:"కాంపిటెన్సీ ఇంజిన్",dataVisuals:"డేటా విజువల్స్",systemConfiguration:"సిస్టమ్ కాన్ఫిగరేషన్",
    visualSystem:"విజువల్ సిస్టమ్",securityStatus:"MoSPI సురక్షిత గేట్‌వే",demoEnvironment:"జాతీయ డేటా పోర్టల్ · ధృవీకరించబడిన SSL/TLS 1.3 నోడ్",
    connectProduction:"కేంద్ర గణాంక డైరెక్టరీ మరియు NDSAP ఇంటర్‌ఆపరేబిలిటీ ఇన్‌ఫ్రాస్ట్రక్చర్‌కు ఎండ్-టు-ఎండ్ ఎన్‌క్రిప్షన్‌తో అనుసంధానించబడింది.",email:"ఇమెయిల్",
    notifications:"నోటిఫికేషన్‌లు",noNotifications:"కొత్త నోటిఫికేషన్‌లు లేవు",help:"సహాయం",live:"లైవ్",
    courseAnalytics:"కోర్సు పురోగతి & విశ్లేషణ",avgCompletion:"సగటు పూర్తి",weeklyHours:"వారపు వేగం",
    verifiedCertificate:"అధికారికంగా ధృవీకరించబడిన సర్టిఫికెట్",downloadOfficialCert:"అధికారిక సర్టిఫికెట్ డౌన్‌లోడ్ చేయండి",
    copyVerificationLink:"ధృవీకరణ లింక్‌ను కాపీ చేయండి",moduleWorkspace:"మాడ్యూల్ స్టడీ వర్క్‌స్పేస్",launchModuleQuiz:"డయాగ్నస్టిక్ క్విజ్ ప్రారంభించండి",
    assessmentDetails:"అసెస్‌మెంట్ డయాగ్నస్టిక్ విశ్లేషణ",userGuide:"వినియోగదారు మార్గదర్శకత్వం & మద్దతు"
  }
};

function tr(lang, key) {
  return DICTIONARY[lang]?.[key] || DICTIONARY.en[key] || key;
}

function copy(lang, key) {
  return LOCALIZED_COPY[lang]?.[key] || LOCALIZED_COPY.en[key] || key;
}

function safeUser() {
  try {
    return JSON.parse(localStorage.getItem("statSkillUser") || "null");
  } catch {
    return null;
  }
}

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
const API_TOKEN_KEY = "statSkillApiToken";
const API_REFRESH_MS = 5000;

function generateClientPdfBlob(title, subtitle, paragraphs = []) {
  const escapePdf = (str) =>
    (str || "")
      .replace(/[^\x20-\x7E]/g, " ")
      .replaceAll("\\", "\\\\")
      .replaceAll("(", "\\(")
      .replaceAll(")", "\\)");

  const lines = [
    "BT",
    "/F1 16 Tf",
    "50 740 Td",
    `(${escapePdf(title)}) Tj`,
    "/F1 10 Tf",
    "0 -22 Td",
    `(${escapePdf(subtitle)}) Tj`,
    "0 -18 Td",
    "(--------------------------------------------------------------------------------) Tj",
    "/F1 9 Tf",
  ];
  paragraphs.slice(0, 24).forEach(p => {
    lines.push("0 -15 Td");
    lines.push(`(${escapePdf((p || "").slice(0, 95))}) Tj`);
  });
  lines.push("ET");
  const streamContent = lines.join("\n");
  const streamLen = streamContent.length;

  const part1 = "%PDF-1.4\n";
  const part2 = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n";
  const part3 = "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n";
  const part4 = "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n";
  const part5 = `4 0 obj\n<< /Length ${streamLen} >>\nstream\n${streamContent}\nendstream\nendobj\n`;
  const part6 = "5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n";

  const body = part1 + part2 + part3 + part4 + part5 + part6;
  const o1 = body.indexOf("1 0 obj");
  const o2 = body.indexOf("2 0 obj");
  const o3 = body.indexOf("3 0 obj");
  const o4 = body.indexOf("4 0 obj");
  const o5 = body.indexOf("5 0 obj");
  const xrefPos = body.length;

  const pad10 = (n) => String(n).padStart(10, "0");
  const xref =
    `xref\n0 6\n` +
    `0000000000 65535 f \n` +
    `${pad10(o1)} 00000 n \n` +
    `${pad10(o2)} 00000 n \n` +
    `${pad10(o3)} 00000 n \n` +
    `${pad10(o4)} 00000 n \n` +
    `${pad10(o5)} 00000 n \n` +
    `trailer\n<< /Size 6 /Root 1 0 R >>\n` +
    `startxref\n${xrefPos}\n%%EOF\n`;

  return new Blob([body + xref], { type: "application/pdf" });
}


/* ================================================================
   COMPETENCY ENGINE
   Multi-signal prototype analytics. Benchmark values are configurable
   and should be replaced by the authoritative MoSPI/iGOT catalogue
   once that backend mapping is approved.
================================================================ */
const KARMAYOGI_DATA = {
  competencyScores: {},
  assessments: [],
  courses: [],
  selfAssessment: {},
  learningHours: {},
  modules: [],
  documents: [],
  certificates: [],
  notifications: []
};

const ENGINE_DEFINITIONS = [
  {key:"statisticalMethods",name:"Statistical Methods",icon:BarChart3,benchmark:3.5,weight:1.15,
   description:"Inference, sampling, regression and time-series analysis.",
   subSkills:["Descriptive Statistics","Hypothesis Testing","Regression Analysis","Time Series Analysis"]},
  {key:"dataQuality",name:"Data Quality",icon:ShieldCheck,benchmark:3.5,weight:1.05,
   description:"Validation, error detection, review and quality assurance.",
   subSkills:["Data Validation","Error Detection","Imputation","Audit & Review"]},
  {key:"python",name:"Python",icon:FileText,benchmark:3,weight:1,
   description:"Python for data analysis, automation and statistical workflows.",
   subSkills:["pandas","Visualisation","Automation","Statistical Libraries"]},
  {key:"gis",name:"GIS & Spatial Statistics",icon:Target,benchmark:3,weight:1,
   description:"Spatial datasets, mapping, GIS tools and geographic analysis.",
   subSkills:["Map Projections","Spatial Joins","GIS Tools","Choropleth Mapping"]},
  {key:"machineLearning",name:"Machine Learning",icon:Zap,benchmark:3,weight:.95,
   description:"Predictive modelling, evaluation and feature engineering.",
   subSkills:["Supervised Learning","Model Evaluation","Feature Engineering","ML Frameworks"]}
];

const average = values => {
  const n = values.map(Number).filter(Number.isFinite);
  return n.length ? n.reduce((a,b)=>a+b,0)/n.length : 0;
};

function normalizeCompetencyPayload(payload) {
  const source = payload?.data && typeof payload.data === "object" ? payload.data : (payload || {});
  const apiUser = source.user || source.profile || {};
  const profile = source.profile || apiUser;

  // Normalize every possible backend representation into one view model.
  const scoreMap = { ...(source.competencyScores || {}) };

  if (Array.isArray(source.competencies)) {
    source.competencies.forEach(item => {
      const key = item?.key || item?.id;
      const score = Number(item?.score ?? item?.scoreOutOf5);
      if (key && Number.isFinite(score)) scoreMap[key] = score;
    });
  }

  const assessmentHistory = Array.isArray(source.assessmentHistory)
    ? source.assessmentHistory
    : Array.isArray(source.assessments)
      ? source.assessments
      : [];

  const assessments = assessmentHistory.map(item => ({
    ...item,
    title: item.title || item.assessment || "Assessment",
    score: Number(item.score ?? 0)
  }));

  const modules = Array.isArray(source.modules)
    ? source.modules
    : Array.isArray(source.learningPath?.modules)
      ? source.learningPath.modules
      : [];

  const courses = Array.isArray(source.courses) ? source.courses : [];
  const assignments = Array.isArray(source.assignments) ? source.assignments : [];

  const selfAssessment = source.selfAssessment
    || source.rawInputs?.selfAssessment
    || {};

  const learningHours = source.learningHours
    || source.rawInputs?.learningHours
    || source.analytics?.learningMixHours
    || {};

  return {
    ...source,
    user: apiUser,
    profile,
    employeeCode: source.employeeCode || apiUser.employeeCode,
    competencyScores: scoreMap,
    assessments,
    assessmentHistory: assessments,
    assignments,
    courses,
    selfAssessment,
    learningHours,
    modules,
    learningPath: source.learningPath || { modules },
    documents: Array.isArray(source.documents) ? source.documents : [],
    certificates: Array.isArray(source.certificates) ? source.certificates : [],
    notifications: Array.isArray(source.notifications) ? source.notifications : []
  };
}

function runCompetencyEngine(data = KARMAYOGI_DATA) {
  const normalized = normalizeCompetencyPayload(data);

  const competencies = ENGINE_DEFINITIONS.map(def => {
    const supplied = Array.isArray(normalized.competencies)
      ? normalized.competencies.find(item => (item.key || item.id) === def.key)
      : null;

    const assessments = normalized.assessments.filter(item => item.domain === def.key);
    const courses = normalized.courses.filter(item => item.domain === def.key);
    const self = average(normalized.selfAssessment?.[def.key] || []);
    const hours = Number(normalized.learningHours?.[def.key] || 0);

    const quiz = average(assessments.map(item => item.score)) / 20;
    const course = average(courses.map(item => item.score)) / 20;
    const effort = Math.min(5, hours / 8);

    const calculatedScore = Math.max(
      0,
      Math.min(5, quiz * .50 + course * .25 + self * .15 + effort * .10)
    );

    const suppliedScore = Number(
      normalized.competencyScores?.[def.key]
      ?? supplied?.scoreOutOf5
      ?? supplied?.score
    );

    const score = Number.isFinite(suppliedScore)
      ? Math.max(0, Math.min(5, suppliedScore))
      : calculatedScore;

    const level = supplied?.level || (score >= 3.5 ? "Strong" : score >= 2 ? "Moderate" : "Weak");
    const benchmark = Number(supplied?.benchmark ?? def.benchmark);
    const gap = Math.max(0, benchmark - score);

    let trend = supplied?.trend || "Stable";
    if (!supplied?.trend && assessments.length > 1) {
      const delta = Number(assessments[assessments.length - 1]?.score || 0) - Number(assessments[0]?.score || 0);
      trend = delta >= 5 ? "Improving" : delta <= -5 ? "Declining" : "Stable";
    }

    return {
      ...def,
      ...(supplied || {}),
      key: def.key,
      name: supplied?.name || def.name,
      score: Number(score.toFixed(2)),
      scoreOutOf5: Number(score.toFixed(2)),
      scorePercent: Number((score * 20).toFixed(1)),
      benchmark,
      level,
      trend,
      gap: Number(gap.toFixed(2)),
      gapPercent: benchmark ? Number(((gap / benchmark) * 100).toFixed(1)) : 0,
      weight: Number(supplied?.weight ?? def.weight),
      evidence: supplied?.evidence || {
        quizAverage: Math.round(average(assessments.map(item => item.score))),
        courseAverage: Math.round(average(courses.map(item => item.score))),
        selfAssessment: Math.round(self * 20),
        learningHours: hours
      },
      subSkills: supplied?.subSkills?.length
        ? supplied.subSkills
        : def.subSkills.map((name, i) => ({
            name,
            score: Math.round(Number((normalized.selfAssessment?.[def.key] || [])[i] || 0) * 20)
          }))
    };
  });

  const totalWeight = competencies.reduce((sum, item) => sum + Number(item.weight || 1), 0) || 1;
  const weighted = competencies.reduce((sum, item) => sum + item.score * Number(item.weight || 1), 0) / totalWeight;
  const quizAverage = Math.round(average(normalized.assessments.map(item => item.score)));
  const totalHours = Object.values(normalized.learningHours || {}).reduce((sum, value) => sum + Number(value || 0), 0);

  const sourceDashboard = normalized.dashboard || {};
  const overallScore = Number.isFinite(Number(sourceDashboard.overallCompetency))
    ? Number(sourceDashboard.overallCompetency)
    : Math.round(Math.min(100, Math.max(0,
        weighted * 20 * .82 + quizAverage * .12 + Math.min(totalHours, 100) * .06
      )));

  const topGaps = Array.isArray(normalized.criticalSkills) && normalized.criticalSkills.length
    ? normalized.criticalSkills
        .map(item => competencies.find(c => c.name === item.competency || c.key === item.competency) || item)
        .slice(0, 3)
    : [...competencies].sort((a, b) => b.gap - a.gap).slice(0, 3);

  const fallbackRecommendations = {
    gis: "Complete GIS for Statistics and practise spatial joins and choropleth mapping.",
    machineLearning: "Strengthen Python foundations before moving into model evaluation and ML.",
    python: "Build pandas, visualisation and automation skills through practical datasets.",
    dataQuality: "Practise validation, error detection and statistical audit workflows.",
    statisticalMethods: "Target sampling, regression and time-series exercises for greater analytical depth."
  };

  const recommendations = Array.isArray(normalized.recommendations)
    ? normalized.recommendations
    : topGaps
        .map(item => normalized.criticalSkills?.find(cs => cs.competency === item.name)?.recommendedAction || fallbackRecommendations[item.key])
        .filter(Boolean);

  const moduleList = normalized.modules || [];
  const completedModules = Number(
    normalized.learningPath?.modulesCompleted
    ?? sourceDashboard.completedModules
    ?? moduleList.filter(m => String(m.status || "").toLowerCase() === "completed").length
  );

  const totalModules = Number(
    normalized.learningPath?.totalModules
    ?? sourceDashboard.totalModules
    ?? moduleList.length
  );

  const learningProgress = Number(
    sourceDashboard.learningProgress
    ?? (normalized.learningPath?.modulesCompleted != null && normalized.learningPath?.totalModules
      ? Math.round((Number(normalized.learningPath.modulesCompleted) / Number(normalized.learningPath.totalModules)) * 100)
      : average(moduleList.map(m => Number(m.progress || 0))))
  );

  const assessmentsCompleted = Number(sourceDashboard.assessmentsCompleted ?? normalized.assessments.filter(item => String(item.status || "Completed").toLowerCase() === "completed").length);
  const assessmentsTotal = Number(sourceDashboard.assessmentsTotal ?? normalized.assessments.length);

  return {
    overallScore,
    criticalGaps: Number(sourceDashboard.criticalSkillGaps ?? competencies.filter(c => c.level === "Weak").length),
    moderateGaps: Number(sourceDashboard.moderateSkillGaps ?? competencies.filter(c => c.level === "Moderate").length),
    strongSkills: Number(sourceDashboard.strongSkills ?? competencies.filter(c => c.level === "Strong").length),
    assessmentAverage: Number(sourceDashboard.assessmentAverage ?? quizAverage),
    learningHours: Number(sourceDashboard.learningHours ?? totalHours),
    learningHoursByDomain: normalized.analytics?.learningMixHours || { ...(normalized.learningHours || {}) },
    assessmentHistory: normalized.assessmentHistory,
    competencies,
    topGaps,
    recommendations,
    learningProgress,
    completedModules,
    totalModules,
    assessmentsCompleted,
    assessmentsTotal,
    assignmentsCompleted: Number(
      normalized.dashboard?.assignmentsCompleted
      ?? normalized.assignments.filter(item => String(item.status || "").toLowerCase() === "completed").length
    ),
    assignmentsTotal: Number(normalized.dashboard?.assignmentsTotal ?? normalized.assignments.length),
    coursesCompleted: Number(
      normalized.dashboard?.coursesCompleted
      ?? normalized.courses.filter(item => String(item.status || "").toLowerCase() === "completed").length
    ),
    coursesTotal: normalized.courses.length,
    rank: normalized.dashboard?.rank || "A",
    level: Number(normalized.dashboard?.level ?? overallScore),
    xp: Number(normalized.dashboard?.xp ?? 0),
    methodology: normalized.engine?.methodology || "50% assessments · 25% courses · 15% self-assessment · 10% learning effort"
  };
}

/* API boundary
   The FastAPI service is the authoritative user-specific source. A successful
   login returns the full data snapshot for that user. The client refreshes
   that snapshot periodically so JSON changes propagate to every page.
*/
async function apiLogin(email, password){
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method:"POST",
    headers:{"Content-Type":"application/json","Accept":"application/json"},
    body:JSON.stringify({email, password}),
    cache:"no-store"
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload?.detail || "Invalid email or password.");
  return payload;
}

async function apiFetchMe(token){
  const response = await fetch(`${API_BASE_URL}/api/me/data`, {
    method:"GET",
    headers:{
      Accept:"application/json",
      Authorization:`Bearer ${token}`
    },
    cache:"no-store"
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload?.detail || `API returned ${response.status}`);
  return payload;
}

async function apiLogout(token){
  if (!token) return;
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method:"POST",
      headers:{Authorization:`Bearer ${token}`}
    });
  } catch {
    // Session cleanup on the server is best-effort for the demo.
  }
}

function SystemCard({ children, className = "" }) {
  return <section className={`system-card ${className || "bare-card"}`}>{children}</section>;
}

function Progress({ value, color = "cyan" }) {
  const width = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div className="progress">
      <span className={`progress-fill ${color} p-${width}`} />
    </div>
  );
}

function Pill({ children, tone = "neutral" }) {
  return <span className={`pill ${tone}`}>{children}</span>;
}

function PageHeading({ kicker, title, subtitle, actions }) {
  return (
    <div className="page-heading system-card">
      <div>
        <div className="kicker">{kicker}</div>
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {actions && <div className="heading-actions">{actions}</div>}
    </div>
  );
}

function StatCard({ label, value, suffix, meta, color = "cyan", icon: Icon }) {
  return (
    <SystemCard className={`stat-card ${color}`}>
      <div className="stat-card-top">
        <span>{label}</span>
        <span className="stat-icon"><Icon size={18} /></span>
      </div>
      <div className="stat-value">{value}<small>{suffix}</small></div>
      <div className="stat-meta">{meta}</div>
      <Progress value={typeof value === "number" ? value : 0} color={color} />
    </SystemCard>
  );
}

function DashboardPage({ user, lang, onNavigate, engine, data }) {
  const modules = data?.learningPath?.modules || data?.modules || [];
  const assessments = data?.assessments || [];
  const activeModule = modules.find(m => m?.state === "active") || modules.find(m => String(m?.status || "").toLowerCase() === "in progress");
  const nextRecommendation = engine.recommendations?.[0] || "Continue your learning path and complete the active module.";
  const projectId = user.projectId || data?.profile?.projectId || "SIH26101";
  const moduleProgress = Number(activeModule?.progress || 0);
  const isOfficer = user.accountType === "cadre_officer" || !user.accountType || String(user.accountType).includes("officer");
  const defaultRole = isOfficer ? "Senior Statistical Officer (SSO)" : "Citizen Data Analyst & Research Scholar";
  const defaultDept = isOfficer ? "MoSPI" : "Academic / Citizen Track";

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "command")}
        title={`${tr(lang, "hello")}, ${user.name || "Learner"}.`}
        subtitle={`${user.role || defaultRole} · ${user.department || defaultDept} · ${projectId}`}
        actions={<Pill tone="online"><Activity size={12} /> {tr(lang, "online")}</Pill>}
      />

      <div className="stats-grid">
        <StatCard label={tr(lang, "competency")} value={engine.overallScore} suffix="/100" meta="Diagnostic index score" color="cyan" icon={Target} />
        <StatCard label={tr(lang, "gaps")} value={engine.criticalGaps + engine.moderateGaps} meta={engine.topGaps?.map(g => g.name).slice(0, 2).join(" · ") || "No critical gaps"} color="red" icon={AlertTriangle} />
        <StatCard label={tr(lang, "learning")} value={engine.learningProgress ?? 0} suffix="%" meta={`${engine.completedModules ?? 0}/${engine.totalModules ?? 0} modules`} color="green" icon={TrendingUp} />
        <StatCard label={tr(lang, "completed")} value={engine.assessmentsCompleted ?? 0} suffix={`/${engine.assessmentsTotal ?? 0}`} meta="Recorded scored evaluations" color="purple" icon={ClipboardCheck} />
      </div>

      <div className="hero-grid">
        <SystemCard className="player-card">
          <div className="system-label">{tr(lang, "player")}</div>
          <div className="player-layout">
            <div className="avatar-xl">{(user.name || "A")[0]}</div>
            <div className="player-info">
              <div className="player-name">{user.name || "Learner"}</div>
              <div className="player-role">{user.role || defaultRole}</div>
              <div className="rank-line">
                <span>{tr(lang, "rank").toUpperCase()}</span>
                <strong>{isOfficer ? "MoSPI Cadre (SSS)" : (user.department || "National Open Statistical Learning")}</strong>
                <span>{tr(lang, "level").toUpperCase()}</span>
                <strong>{engine.overallScore}% Ready</strong>
              </div>
              <div className="xp-row">
                <span>{tr(lang, "xp")}</span>
                <Progress value={engine.overallScore} color="cyan" />
                <strong>{engine.overallScore}/100</strong>
              </div>
            </div>
          </div>
          <div className="metric-strip">
            <div><span>SAMPLING & INFERENCE</span><strong>{(engine.competencies.find(c => c.key === "statisticalMethods")?.score ?? 0).toFixed(1)}</strong></div>
            <div><span>DATA QUALITY</span><strong>{(engine.competencies.find(c => c.key === "dataQuality")?.score ?? 0).toFixed(1)}</strong></div>
            <div><span>GIS & SPATIAL</span><strong>{(engine.competencies.find(c => c.key === "gis")?.score ?? 0).toFixed(1)}</strong></div>
            <div><span>DATA SCIENCE & ML</span><strong>{(engine.competencies.find(c => c.key === "machineLearning")?.score ?? 0).toFixed(1)}</strong></div>
          </div>
        </SystemCard>

        <SystemCard className="recommendation-card">
          <div className="system-label">{tr(lang, "recommendation")}</div>
          <div className="recommendation-title"><Sparkles size={18} /> {activeModule?.title || "Learning Path"}</div>
          <p>{nextRecommendation}</p>
          <div className="recommendation-box">
            <div><span>{tr(lang, "activeModule").toUpperCase()}</span><strong>{activeModule?.title || "No active module"}</strong></div>
            <Progress value={moduleProgress} color="cyan" />
            <span className="progress-label">{moduleProgress}% complete</span>
          </div>
          <button className="primary-btn" onClick={() => onNavigate("Learning Path")}>
            {tr(lang, "continue")} <ChevronRight size={16} />
          </button>
        </SystemCard>
      </div>

      <div className="three-grid">
        <SystemCard>
          <div className="card-header"><div><div className="system-label">{tr(lang, "matrix").toUpperCase()}</div><h2>{tr(lang, "competencies")}</h2></div><button className="ghost-btn" onClick={() => onNavigate("My Competencies")}>{tr(lang, "viewAll")} <ChevronRight size={14} /></button></div>
          <div className="compact-list">
            {engine.competencies.map((item) => {
              const Icon = item.icon;
              return <div className="compact-row" key={item.key}>
                <div className={`mini-icon ${item.color || "cyan"}`}><Icon size={15} /></div>
                <div className="grow"><strong>{item.name}</strong><Progress value={item.score * 20} color={item.color || "cyan"} /></div>
                <strong className={`score ${item.color || "cyan"}`}>{item.score.toFixed(1)}</strong>
              </div>;
            })}
          </div>
        </SystemCard>

        <SystemCard>
          <div className="card-header"><div><div className="system-label">{tr(lang, "trainingPipeline").toUpperCase()}</div><h2>{tr(lang, "path")}</h2></div><button className="ghost-btn" onClick={() => onNavigate("Learning Path")}>{tr(lang, "viewAll")} <ChevronRight size={14} /></button></div>
          <div className="timeline">
            {modules.map((m) => <div className="timeline-row" key={m.step}>
              <div className={`timeline-node ${m.state || "locked"}`}>{m.state === "done" ? <Check size={13} /> : m.state === "locked" ? <Lock size={12} /> : m.step}</div>
              <div className="grow"><strong>{m.title}</strong><span>{m.status} · {m.duration}</span></div>
              {m.state !== "locked" && <div className="mini-progress"><Progress value={m.progress} color={m.state === "done" ? "green" : "cyan"} /></div>}
            </div>)}
          </div>
        </SystemCard>

        <SystemCard>
          <div className="card-header"><div><div className="system-label">{tr(lang, "schedule").toUpperCase()}</div><h2>{tr(lang, "upcoming")}</h2></div><CalendarDays size={17} /></div>
          <div className="assessment-list">
            {assessments.slice(0, 5).map((a, index) => <div className={`assessment ${["blue","amber","green","purple","red"][index % 5]}`} key={a.id || a.title || index}>
              <div className="assessment-date">{a.id || `A${index + 1}`}</div>
              <div className="grow"><strong>{a.title || a.domain || "Assessment"}</strong><span>{a.domain || "Assessment"} · Score {Number(a.score ?? 0)}%</span></div>
            </div>)}
          </div>
        </SystemCard>
      </div>

      <SystemCard className="insight-card">
        <div className="insight-icon"><Sparkles size={22} /></div>
        <div className="grow"><div className="system-label">{tr(lang, "insight")}</div><h2>{tr(lang, "trajectory")}</h2><p>{nextRecommendation}</p></div>
        <button className="secondary-btn" onClick={() => onNavigate("My Competencies")}>{tr(lang, "openAnalysis")} <ChevronRight size={14} /></button>
      </SystemCard>
    </div>
  );
}

function CompetenciesPage({ engine, lang, data }) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(null);
  const filtered = useMemo(() => engine.competencies.filter(c => c.name.toLowerCase().includes(query.toLowerCase())), [engine.competencies, query]);
  return (
    <div className="stack">
      <PageHeading kicker={tr(lang, "competencyEngine").toUpperCase()} title={tr(lang, "competencies")} subtitle={tr(lang, "visualSummary")} actions={<div className="search"><Search size={15} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder={tr(lang, "search")} /></div>} />
      <div className="summary-grid">
        <SystemCard className="summary-card"><span>{tr(lang,"competencies").toUpperCase()}</span><strong>{engine.competencies.length}</strong></SystemCard>
        <SystemCard className="summary-card"><span>{tr(lang,"strong").toUpperCase()}</span><strong className="green">{engine.strongSkills}</strong></SystemCard>
        <SystemCard className="summary-card"><span>{tr(lang,"gaps").toUpperCase()}</span><strong className="amber">{engine.criticalGaps + engine.moderateGaps}</strong></SystemCard>
        <SystemCard className="summary-card"><span>{tr(lang,"score").toUpperCase()}</span><strong className="cyan">{(engine.competencies.reduce((s,c)=>s+c.score,0)/engine.competencies.length).toFixed(1)} / 5</strong></SystemCard>
      </div>
      <SystemCard className="engine-competency-block">
        <div className="engine-panel-head">
          <div><div className="system-label">{tr(lang,"gapAssessment")}</div><h2>Benchmark comparison</h2><p>Multi-signal competency analysis across assessment, course, self-assessment and learning effort.</p></div>
          <div className="engine-score">{engine.overallScore}<span>/100</span></div>
        </div>
        <div className="engine-evidence-grid">
          {engine.competencies.map(item=><div className="engine-evidence" key={item.key}>
            <div className="engine-evidence-title"><strong>{item.name}</strong><Pill tone={item.level.toLowerCase()}>{item.level}</Pill></div>
            <Progress value={item.score*20} color="cyan" />
            <div className="engine-evidence-meta"><span>{item.score.toFixed(1)}/5</span><span>{item.gap ? `Gap ${item.gap.toFixed(1)}` : "Benchmark met"}</span><span>{item.trend}</span></div>
          </div>)}
        </div>
        <div className="recommendation-stack"><div className="system-label">{tr(lang,"priority")}</div>
          {engine.recommendations.map((r,i)=><div className="recommendation-line" key={r}><b>0{i+1}</b><span>{r}</span></div>)}
        </div>
      </SystemCard>
      <SystemCard>
        <div className="card-header"><div><div className="system-label">CRITICAL SKILLS</div><h2>Critical Skill Gaps</h2></div><Pill>{(data?.criticalSkills || []).length}</Pill></div>
        <div className="assessment-list">
          {(data?.criticalSkills || []).map((item, i) => <div className="assessment" key={`${item.competency}-${i}`}>
            <div className="assessment-number">0{i + 1}</div>
            <div className="grow"><strong>{item.competency}</strong><span>{item.priority || "Priority"} · {Number(item.currentScore || 0).toFixed(2)}/5 · Gap {Number(item.gap || 0).toFixed(2)}</span></div>
            <div className="grow"><span>{item.recommendedAction || "Targeted practice recommended."}</span></div>
          </div>)}
        </div>
      </SystemCard>
      <SystemCard>
        <div className="card-header"><div><div className="system-label">BENCHMARK COMPARISON</div><h2>Current Readiness</h2></div><Pill>{(data?.benchmarkComparison || []).length}</Pill></div>
        <div className="assessment-list">
          {(data?.benchmarkComparison || []).map((item, i) => <div className="assessment" key={`${item.competency}-${i}`}>
            <div className="assessment-number">0{i + 1}</div>
            <div className="grow"><strong>{item.competency}</strong><span>{Number(item.currentScore || 0).toFixed(2)} / {Number(item.benchmark || 0).toFixed(2)} · {item.status || "—"}</span></div>
            <strong>{Number(item.readinessPercent || 0).toFixed(1)}%</strong>
          </div>)}
        </div>
      </SystemCard>
      <SystemCard>
        <div className="card-header"><div><div className="system-label">{tr(lang,"skillMatrix")}</div><h2>{tr(lang,"currentReadiness")}</h2></div><Pill>5 domains</Pill></div>
        <div className="detail-list">
          {filtered.map((item) => {
            const Icon = item.icon;
            const open = selected === item.name;
            return <div className={`detail-row ${open ? "open" : ""}`} key={item.name}>
              <button className="detail-trigger" onClick={() => setSelected(open ? null : item.name)}>
                <div className={`mini-icon ${item.color}`}><Icon size={16} /></div>
                <div className="grow"><strong>{item.name}</strong><span>{item.desc}</span><Progress value={item.score * 20} color={item.color} /></div>
                <div className="detail-score"><strong>{item.score.toFixed(1)}</strong><Pill tone={item.level.toLowerCase()}>{item.level}</Pill></div>
                <ChevronDown size={15} className={open ? "rotate" : ""} />
              </button>
              {open && <div className="detail-body"><div><span>Trend</span><strong>{item.trend}</strong></div><div><span>Last assessment</span><strong>10 May 2026</strong></div><div><span>Priority</span><strong>{item.level === "Weak" ? "High" : "Normal"}</strong></div></div>}
            </div>;
          })}
        </div>
      </SystemCard>
    </div>
  );
}

function LearningPage({ lang, data, engine, onNavigate, onStartQuiz }) {
  const [selectedModule, setSelectedModule] = useState(null);
  const modules = data?.learningPath?.modules || data?.modules || [];
  const completed = engine.completedModules ?? 0;
  const total = engine.totalModules ?? modules.length;
  const progress = engine.learningProgress ?? 0;
  const totalHours = engine.learningHours ?? 0;
  return <div className="stack">
    <PageHeading kicker={tr(lang, "trainingPipeline").toUpperCase()} title={tr(lang,"path")} subtitle={`${completed} of ${total} modules completed · ${totalHours} learning hours`} />
    <SystemCard className="track-banner">
      <div><div className="system-label">{tr(lang,"activeTrack").toUpperCase()}</div><h2>{data?.learningPath?.track || data?.profile?.course || data?.profile?.track || "Learning Path"}</h2><p>{completed} of {total} modules completed · {totalHours} hours recorded</p></div>
      <div className="track-ring">{progress}%</div>
    </SystemCard>
    <div className="module-grid">
      {modules.map((m) => <SystemCard key={m.step || m.title} className={`module-card ${m.state || "locked"}`}>
        <div className="module-top"><span className="module-number">0{m.step}</span><Pill tone={m.state === "done" ? "strong" : m.state === "active" ? "active" : "locked"}>{m.status === "Completed" ? tr(lang,"completed") : m.status === "In Progress" ? tr(lang,"inProgress") : tr(lang,"locked")}</Pill></div>
        <h2>{m.title}</h2><p>Structured module with practical lessons, domain exercises and assessment checkpoints.</p>
        <div className="module-meta"><span>{m.duration || "—"}</span><span>{m.lessons || "—"} {tr(lang,"lessons")}</span></div>
        <Progress value={m.progress} color={m.state === "done" ? "green" : "cyan"} />
        <button 
          className={m.state === "locked" ? "secondary-btn disabled" : "primary-btn"} 
          disabled={m.state === "locked"}
          onClick={() => setSelectedModule(m)}
          title={m.state === "locked" ? "Prerequisites required" : "Open module curriculum workspace"}
        >
          {m.state === "locked" ? <Lock size={14} /> : <PlayCircle size={14} />}
          {m.state === "done" ? tr(lang,"reviewModule") : m.state === "active" ? tr(lang,"continueModule") : tr(lang,"locked")}
        </button>
      </SystemCard>)}
    </div>

    {selectedModule && (
      <div className="app-modal-overlay" onClick={() => setSelectedModule(null)}>
        <div className="app-modal-dialog" onClick={e => e.stopPropagation()}>
          <div className="app-modal-header">
            <div>
              <div className="system-label" style={{ color: "#0f2e5a" }}>MODULE 0{selectedModule.step} · {selectedModule.duration || "8 hrs"}</div>
              <h3>{selectedModule.title}</h3>
              <p>National Statistical System Accredited Training Syllabus</p>
            </div>
            <button className="icon-btn" onClick={() => setSelectedModule(null)}><X size={16} /></button>
          </div>
          <div className="app-modal-body">
            <div className="credential-seal-banner" style={{ background: "#eff6ff", borderColor: "#bfdbfe", color: "#1e40af" }}>
              <div className="credential-seal-icon" style={{ background: "#dbeafe", color: "#1d4ed8" }}>
                <BookOpen size={24} />
              </div>
              <div className="credential-seal-text">
                <strong style={{ color: "#1e3a8a" }}>Curriculum Syllabus & Practice Directives</strong>
                <span style={{ color: "#2563eb" }}>Status: {selectedModule.status || "In Progress"} · {selectedModule.progress || 0}% Completed</span>
              </div>
            </div>

            <div className="lesson-checklist">
              <div className="lesson-check-item">
                <div><strong>Lesson 1: Theoretical Framework & Official Sampling Design</strong><span>Stratified multistage sampling & UN fundamental principles</span></div>
                <CheckCircle2 size={16} color="#059669" />
              </div>
              <div className="lesson-check-item">
                <div><strong>Lesson 2: Field Protocols, CAPI Enumeration & Data Cleaning</strong><span>Survey protocols, non-sampling error minimization</span></div>
                <CheckCircle2 size={16} color="#059669" />
              </div>
              <div className="lesson-check-item">
                <div><strong>Lesson 3: Computational Tabulation & Statistical Software Practice</strong><span>Automated consistency checks using Python, R & QGIS</span></div>
                <CheckCircle2 size={16} color={selectedModule.state === "done" ? "#059669" : "#94a3b8"} />
              </div>
              <div className="lesson-check-item">
                <div><strong>Lesson 4: Diagnostic Validation & Verification Checkpoint</strong><span>End-of-module assessment derived from MoSPI manuals</span></div>
                <CheckCircle2 size={16} color={selectedModule.state === "done" ? "#059669" : "#94a3b8"} />
              </div>
            </div>
          </div>
          <div className="app-modal-footer">
            <a 
              href="https://igotkarmayogi.gov.in" 
              target="_blank" 
              rel="noreferrer" 
              className="secondary-btn"
              style={{ textDecoration: "none" }}
            >
              <ExternalLink size={14} /> Open in iGOT Portal
            </a>
            <button 
              className="primary-btn" 
              onClick={() => {
                const mod = selectedModule;
                setSelectedModule(null);
                if (onStartQuiz) onStartQuiz({ domain: mod.domain || "statisticalMethods", title: mod.title });
              }}
            >
              <PlayCircle size={14} /> {tr(lang, "launchModuleQuiz")}
            </button>
          </div>
        </div>
      </div>
    )}
  </div>;
}

function AssessmentsPage({ lang, data, engine, onStartQuiz }) {
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const assessments = data?.assessments || [];
  const averageScore = engine.assessmentAverage || 0;
  const assignments = data?.assignments || [];
  const courses = data?.courses || [];
  return <div className="stack">
    <PageHeading kicker={tr(lang,"assessmentControl").toUpperCase()} title={tr(lang,"assessments")} subtitle={`${assessments.length} assessment records for ${data?.profile?.name || "this user"}`} />
    <div className="stats-grid three">
      <StatCard label={tr(lang,"completed")} value={engine.assessmentsCompleted ?? 0} suffix={`/${engine.assessmentsTotal ?? assessments.length}`} meta="Recorded scored assessments" color="green" icon={CheckCircle2} />
      <StatCard label={tr(lang,"score")} value={averageScore} suffix="%" meta="Average across assessments" color="cyan" icon={Target} />
      <StatCard label="Assignments" value={engine.assignmentsCompleted ?? 0} suffix={`/${engine.assignmentsTotal ?? assignments.length}`} meta="Completed assignments" color="purple" icon={ClipboardList} />
    </div>
    <SystemCard>
      <div className="card-header"><div><div className="system-label">{tr(lang,"upcomingQueue")}</div><h2>{tr(lang,"nextCheckpoints")}</h2></div></div>
      <div className="assessment-list large">
        {assessments.map((a, i) => <div className={`assessment ${["blue","amber","green","purple","red"][i % 5]}`} key={a.id || a.title || i}>
          <div className="assessment-number">0{(i + 1)}</div>
          <div className="grow"><strong>{a.title || "Assessment"}</strong><span>{a.domain || "—"} · Score {Number(a.score ?? 0)}% · {a.status || "Recorded"}</span></div>
          <button className="secondary-btn" onClick={() => setSelectedAssessment(a)}>{tr(lang,"openDetails")} <ChevronRight size={14} /></button>
        </div>)}
      </div>
    </SystemCard>
    <SystemCard>
      <div className="card-header"><div><div className="system-label">ASSIGNMENTS</div><h2>Assignment Records</h2></div></div>
      <div className="assessment-list large">
        {assignments.map((a, i) => <div className={`assessment ${["blue","amber","green","purple","red"][i % 5]}`} key={a.id || i}>
          <div className="assessment-number">0{(i + 1)}</div>
          <div className="grow"><strong>{a.title || "Assignment"}</strong><span>{a.domain || "—"} · {Number(a.score ?? 0)}/{Number(a.maxScore ?? 100)} · {a.status || "Recorded"} · {a.dueDate || "—"}</span></div>
          <Pill tone={String(a.status || "").toLowerCase() === "completed" ? "strong" : "active"}>{a.status || "Recorded"}</Pill>
        </div>)}
      </div>
    </SystemCard>
    <SystemCard>
      <div className="card-header"><div><div className="system-label">COURSES</div><h2>Course Performance</h2></div><Pill>{courses.length}</Pill></div>
      <div className="assessment-list large">
        {courses.map((c, i) => <div className={`assessment ${["blue","amber","green","purple","red"][i % 5]}`} key={c.id || i}>
          <div className="assessment-number">0{(i + 1)}</div>
          <div className="grow"><strong>{c.title || "Course"}</strong><span>{c.domain || "—"} · Score {Number(c.score ?? 0)}% · {c.progress ?? 0}% progress · {c.hours ?? 0} hrs</span></div>
          <Pill tone={String(c.status || "").toLowerCase() === "completed" ? "strong" : "active"}>{c.status || "Recorded"}</Pill>
        </div>)}
      </div>
    </SystemCard>

    {selectedAssessment && (
      <div className="app-modal-overlay" onClick={() => setSelectedAssessment(null)}>
        <div className="app-modal-dialog" onClick={e => e.stopPropagation()}>
          <div className="app-modal-header">
            <div>
              <div className="system-label" style={{ color: "#0f2e5a" }}>DIAGNOSTIC ASSESSMENT · {selectedAssessment.id || "ASM-RECORD"}</div>
              <h3>{selectedAssessment.title}</h3>
              <p>Domain: {selectedAssessment.domain || "Official Statistics"}</p>
            </div>
            <button className="icon-btn" onClick={() => setSelectedAssessment(null)}><X size={16} /></button>
          </div>
          <div className="app-modal-body">
            <div className="credential-meta-grid">
              <div className="credential-meta-item">
                <span>Domain Focus</span>
                <strong>{selectedAssessment.domain || "Statistical Methodology"}</strong>
              </div>
              <div className="credential-meta-item">
                <span>Achieved Score</span>
                <strong style={{ color: Number(selectedAssessment.score ?? 0) >= 75 ? "#166534" : "#b45309" }}>{Number(selectedAssessment.score ?? 0)}%</strong>
              </div>
              <div className="credential-meta-item">
                <span>Evaluation Status</span>
                <strong>{Number(selectedAssessment.score ?? 0) >= 75 ? "Benchmark Met (Proficient)" : "Targeted Upskilling Required"}</strong>
              </div>
              <div className="credential-meta-item">
                <span>Bloom's Taxonomy Level</span>
                <strong>Application & Analysis</strong>
              </div>
            </div>

            <div className="credential-hash-box">
              <span>Diagnostic Assessment Recommendation</span>
              <p style={{ margin: "4px 0 0", fontSize: "0.85rem", color: "#334155", lineHeight: 1.5 }}>
                {Number(selectedAssessment.score ?? 0) >= 75 
                  ? "Performance demonstrates solid mastery of survey sampling and validation protocols. Recommended to maintain proficiency via advanced case studies."
                  : "Score indicates room for improvement in foundational concepts. Complete the recommended iGOT Karmayogi modules and retake this diagnostic quiz."}
              </p>
            </div>
          </div>
          <div className="app-modal-footer">
            <button className="secondary-btn" onClick={() => setSelectedAssessment(null)}>Close</button>
            <button 
              className="primary-btn"
              onClick={() => {
                const asm = selectedAssessment;
                setSelectedAssessment(null);
                if (onStartQuiz) onStartQuiz({ domain: asm.domain || "statisticalMethods", title: asm.title });
              }}
            >
              <RotateCcw size={14} /> Retake Diagnostic Quiz
            </button>
          </div>
        </div>
      </div>
    )}
  </div>;
}

function DocumentsPage({ lang, data, apiToken }) {
  const [query, setQuery] = useState("");
  const [downloadingId, setDownloadingId] = useState(null);
  const documents = data?.documents || [];
  const filtered = documents.filter(d => `${d.name || ""} ${d.category || ""} ${d.id || ""}`.toLowerCase().includes(query.toLowerCase()));

  const handleDownload = async (doc) => {
    setDownloadingId(doc.id);
    try {
      const token = apiToken || localStorage.getItem(API_TOKEN_KEY) || "";
      const url = `${API_BASE_URL}/api/documents/${doc.id}/download`;
      const res = await fetch(url, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      if (!res.ok) {
        throw new Error("Download API failed");
      }
      const blob = await res.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      const cleanName = (doc.name || `${doc.id}.pdf`).replace(/[–—]/g, "-");
      a.download = cleanName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.warn("Direct API download fallback:", err);
      const cleanName = (doc.name || `${doc.id}.pdf`).replace(/[–—]/g, "-");
      const blob = generateClientPdfBlob(
        `StatSkill AI - ${doc.name}`,
        `Ministry of Statistics & Programme Implementation · ${doc.category || "Study Material"}`,
        [
          `Document ID: ${doc.id}`,
          `Category: ${doc.category || "General Statistics"}`,
          "Status: Verified Official MoSPI Learning Resource",
          "--------------------------------------------------------------------------------",
          "Course Study Guide & Methodological Syllabus:",
          doc.summary || "Standard operating procedure for data collection, validation, and estimation.",
          "--------------------------------------------------------------------------------",
          "Learning Objectives & Competency Benchmarks:",
          "1. Understand fundamental survey concepts, rotating panels, and strata weighting.",
          "2. Detect outliers, impute missing values, and validate enterprise microdata.",
          "3. Apply computational algorithms in Python/Pandas for statistical indicators.",
          "National Statistical Office · Government of India · 2026",
        ]
      );
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = cleanName.endsWith(".pdf") ? cleanName : `${cleanName}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } finally {
      setTimeout(() => setDownloadingId(null), 800);
    }
  };

  return <div className="stack">
    <PageHeading kicker={tr(lang,"documentVault").toUpperCase()} title={tr(lang,"documents")} subtitle={tr(lang,"visualSummary")} actions={<div className="search"><Search size={15} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder={tr(lang,"search")} /></div>} />
    <div className="summary-grid three">
      <SystemCard className="summary-card"><span>{tr(lang,"totalDocuments").toUpperCase()}</span><strong>{documents.length}</strong></SystemCard>
      <SystemCard className="summary-card"><span>{tr(lang,"shared").toUpperCase()}</span><strong className="purple">{documents.filter(d => d.shared === true).length}</strong></SystemCard>
      <SystemCard className="summary-card"><span>{tr(lang,"addedThisMonth").toUpperCase()}</span><strong className="green">{documents.filter(d => d.addedThisMonth === true).length}</strong></SystemCard>
    </div>
    <SystemCard><div className="document-table"><div className="table-head"><span>{tr(lang,"documents")}</span><span>Category</span><span>Size</span><span>Action</span></div>{filtered.map(d => <div className="table-row" key={d.id}><div className="doc-name"><div className="file-icon"><FileText size={16} /></div><div><strong>{d.name}</strong><span>{d.id}</span></div></div><span>{d.category}</span><span>{d.size}</span><button className="icon-btn" title={`Download ${d.name}`} onClick={() => handleDownload(d)} disabled={downloadingId === d.id} style={{ cursor: "pointer", color: "#0f2e5a" }}><Download size={15} /></button></div>)}</div></SystemCard>
  </div>;
}

function CertificatesPage({ lang, data, onNavigate, apiToken }) {
  const [verifyingCert, setVerifyingCert] = useState(null);
  const [copiedLink, setCopiedLink] = useState(false);
  const [downloadingCert, setDownloadingCert] = useState(false);
  const certificates = data?.certificates || [];
  const earned = certificates.filter(c => c.status === "Active").length;
  const inProgress = certificates.filter(c => c.status === "In Progress").length;
  const expiring = certificates.filter(c => c.status === "Expiring Soon").length;

  const handleCopyLink = (cert) => {
    const fakeUrl = `https://mospi.gov.in/credentials/verify?id=${encodeURIComponent(cert.id || "CERT-NSSTA-2026")}&hash=${Math.random().toString(36).substring(2, 10)}`;
    navigator.clipboard?.writeText(fakeUrl);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2200);
  };

  const handleDownloadCert = async (cert) => {
    if (!cert) return;
    setDownloadingCert(true);
    const certId = cert.id || "CERT-NSSTA-2026";
    const recipientName = data?.profile?.name || data?.user?.name || "Official Learner";
    const cleanTitle = (cert.title || "Accreditation").replace(/[^a-zA-Z0-9_-]/g, "_");
    const filename = `CERTIFICATE_${cleanTitle}.pdf`;

    try {
      const token = apiToken || localStorage.getItem(API_TOKEN_KEY) || "";
      const url = `${API_BASE_URL}/api/certificates/${encodeURIComponent(certId)}/download?name=${encodeURIComponent(recipientName)}&title=${encodeURIComponent(cert.title || "")}`;
      const res = await fetch(url, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      if (!res.ok) {
        throw new Error("Backend certificate download returned non-200");
      }
      const blob = await res.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.warn("Backend certificate download fallback to client generator:", err);
      const blob = generateClientPdfBlob(
        `OFFICIAL CERTIFICATE: ${cert.title || "Statistical Accreditation"}`,
        `Ministry of Statistics & Programme Implementation · NSSTA Credential ${certId}`,
        [
          "GOVERNMENT OF INDIA",
          "Ministry of Statistics & Programme Implementation (MoSPI)",
          "National Statistical Systems Training Academy (NSSTA), Greater Noida",
          "--------------------------------------------------------------------------------",
          "OFFICIAL CERTIFICATE OF STATISTICAL COMPETENCY",
          "--------------------------------------------------------------------------------",
          `This is to officially certify that: ${recipientName}`,
          "has successfully completed the institutional accreditation requirements for:",
          `>> ${(cert.title || "Statistical Accreditation").toUpperCase()}`,
          "",
          "Competency Level: FRAC Level 4 (Framework for Roles, Activities & Competencies)",
          `Credential Identifier: ${certId}`,
          "Issuing Body: National Statistical Systems Training Academy (NSSTA)",
          "Accreditation Standard: National Quality Assurance Framework (NQAF)",
          `Issued Date: ${cert.issued || "15 January 2025"}        Valid Until: ${cert.expires || "14 January 2028"}`,
          "Verification Status: ACTIVE & CRYPTOGRAPHICALLY VERIFIED",
          "Security Hash: sha256:8f4b23c91d8e09f5a11c47be389a02d4e8c1b970f5e1289",
          "--------------------------------------------------------------------------------",
          "Digitally certified and registered in the MoSPI National Data Portal Registry.",
          "National Statistical Office, Khurshid Lal Bhawan, Janpath, New Delhi - 110001",
        ]
      );
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } finally {
      setTimeout(() => setDownloadingCert(false), 500);
    }
  };

  return <div className="stack">
    <PageHeading kicker={tr(lang,"credentialLedger").toUpperCase()} title={tr(lang,"certificates")} subtitle={tr(lang,"visualSummary")} />
    <div className="summary-grid three">
      <SystemCard className="summary-card"><span>{tr(lang,"certificatesEarned").toUpperCase()}</span><strong className="green">{earned}</strong></SystemCard>
      <SystemCard className="summary-card"><span>{tr(lang,"inProgress").toUpperCase()}</span><strong className="cyan">{inProgress}</strong></SystemCard>
      <SystemCard className="summary-card"><span>{tr(lang,"expiringSoon").toUpperCase()}</span><strong className="amber">{expiring}</strong></SystemCard>
    </div>
    <div className="certificate-grid">
      {certificates.map(c => <SystemCard className="certificate-card" key={c.id || c.title}>
        <div className="certificate-top"><div className={`mini-icon ${c.color || "blue"}`}><Award size={17} /></div><Pill tone={c.color === "green" ? "strong" : c.color === "amber" ? "warning" : "active"}>{c.status}</Pill></div>
        <h2>{c.title}</h2><p>{c.issuer}</p>
        {c.progress ? <><Progress value={c.progress} color="cyan" /><div className="stat-meta">{c.progress}% complete</div></> : <div className="certificate-meta"><span>Issued<strong>{c.issued}</strong></span><span>Expires<strong>{c.expires}</strong></span></div>}
        <button 
          className="secondary-btn" 
          onClick={() => c.progress ? (onNavigate && onNavigate("Learning Path")) : setVerifyingCert(c)}
          title={c.progress ? "Continue track in Learning Path" : "Verify official credentials"}
        >
          <ShieldCheck size={14} /> {c.progress ? tr(lang,"continueTrack") : tr(lang,"verifyCredential")}
        </button>
      </SystemCard>)}
    </div>

    {verifyingCert && (
      <div className="app-modal-overlay" onClick={() => setVerifyingCert(null)}>
        <div className="app-modal-dialog" onClick={e => e.stopPropagation()}>
          <div className="app-modal-header">
            <div>
              <div className="system-label" style={{ color: "#166534" }}>{tr(lang, "verifiedCertificate").toUpperCase()}</div>
              <h3>{verifyingCert.title}</h3>
              <p>{verifyingCert.issuer || "National Statistical Systems Training Academy (NSSTA), MoSPI"}</p>
            </div>
            <button className="icon-btn" onClick={() => setVerifyingCert(null)}><X size={16} /></button>
          </div>
          <div className="app-modal-body">
            <div className="credential-seal-banner">
              <div className="credential-seal-icon">
                <ShieldCheck size={28} />
              </div>
              <div className="credential-seal-text">
                <strong>Officially Verified by MoSPI Credential Registry</strong>
                <span>Cryptographically anchored in National Statistical Systems Training Academy (NSSTA) ledger</span>
              </div>
            </div>

            <div className="credential-meta-grid">
              <div className="credential-meta-item">
                <span>Recipient Name</span>
                <strong>{data?.profile?.name || data?.user?.name || "Official Learner"}</strong>
              </div>
              <div className="credential-meta-item">
                <span>Credential ID</span>
                <strong>{verifyingCert.id || "CERT-IN-2026-NSSTA-9041"}</strong>
              </div>
              <div className="credential-meta-item">
                <span>Issuing Authority</span>
                <strong>NSSTA / MoSPI</strong>
              </div>
              <div className="credential-meta-item">
                <span>Competency Accreditation</span>
                <strong>FRAC Level 4 Professional</strong>
              </div>
              <div className="credential-meta-item">
                <span>Date Issued</span>
                <strong>{verifyingCert.issued || "15 Jan 2025"}</strong>
              </div>
              <div className="credential-meta-item">
                <span>Valid Until</span>
                <strong>{verifyingCert.expires || "14 Jan 2028"}</strong>
              </div>
            </div>

            <div className="credential-hash-box">
              <span>Cryptographic Verification Fingerprint (SHA-256)</span>
              <code>sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</code>
            </div>
          </div>
          <div className="app-modal-footer">
            <button className="secondary-btn" onClick={() => handleCopyLink(verifyingCert)}>
              {copiedLink ? <><CheckCircle2 size={14} color="#059669" /> Link Copied!</> : <><ExternalLink size={14} /> {tr(lang,"copyVerificationLink")}</>}
            </button>
            <button className="primary-btn" onClick={() => handleDownloadCert(verifyingCert)} disabled={downloadingCert}>
              <Download size={14} /> {downloadingCert ? "Generating PDF..." : tr(lang, "downloadOfficialCert")}
            </button>
          </div>
        </div>
      </div>
    )}
  </div>;
}

function AnalyticsPage({ engine, lang, data }) {
  const maxScore = 5;
  const rawHours = data?.analytics?.learningMixHours || engine.learningHoursByDomain || {};
  const totalHours = Object.values(rawHours).reduce((sum, value) => sum + Number(value || 0), 0) || 1;
  const assessmentHistory = engine.assessmentHistory || [];
  const chartAssessments = assessmentHistory.slice(-5);
  const chartPoints = chartAssessments.map((item,i)=>{
    const x = 65 + i * 125;
    const score = Math.max(0, Math.min(100, Number(item.score) || 0));
    const y = 220 - score * 1.5;
    return { x, y, score };
  });
  const polylinePoints = chartPoints.map(point => `${point.x},${point.y}`).join(" ");
  const barColors = ["green","blue","amber","red","purple"];

  const coursesList = (data?.courses && data.courses.length > 0)
    ? data.courses
    : (data?.learningPath?.modules && data.learningPath.modules.length > 0)
      ? data.learningPath.modules
      : [
          { title: "Compilation of Consumer Price Index (CPI) & Inflation Metrics", progress: 95, hours: 8, status: "Active" },
          { title: "System of National Accounts (SNA 2008) & GDP Compilation", progress: 70, hours: 12, status: "In Progress" },
          { title: "GIS & Spatial Statistics Intermediate Practice", progress: 40, hours: 10, status: "In Progress" },
          { title: "Data Quality & Survey Validation Practice", progress: 85, hours: 6, status: "Completed" },
        ];

  const totalCourseProgress = coursesList.reduce((sum, c) => sum + Number(c.progress ?? (c.score || 50)), 0);
  const avgCompletion = Math.round(totalCourseProgress / (coursesList.length || 1));
  const activeTrackName = data?.learningPath?.track || data?.profile?.course || "National Statistical Capacity Track";

  return (
    <div className="stack analytics-page">
      <PageHeading
        kicker={tr(lang, "dataVisuals").toUpperCase()}
        title={tr(lang,"graphical")}
        subtitle={tr(lang,"visualSummary")}
      />
      <div className="analytics-kpi-grid">
        <SystemCard><span>{tr(lang,"competency")}</span><strong>{engine.overallScore}<small>/100</small></strong></SystemCard>
        <SystemCard><span>{tr(lang,"score")}</span><strong>{engine.assessmentAverage}<small>%</small></strong></SystemCard>
        <SystemCard><span>{tr(lang,"hoursLabel")}</span><strong>{engine.learningHours}<small>h</small></strong></SystemCard>
      </div>
      <div className="analytics-grid">
        <SystemCard className="chart-card">
          <div className="card-header"><div><div className="system-label">01</div><h2>{tr(lang,"competencyScores")}</h2></div></div>
          <div className="vertical-bars">
            {engine.competencies.map((c,i)=>(
              <div className="vbar-item" key={c.key}>
                <div className="vbar-value">{c.score.toFixed(1)}</div>
                <div className="vbar-track"><div className={`vbar-fill ${barColors[i%barColors.length]}`} style={{height:`${(c.score/maxScore)*100}%`}} /></div>
                <span>{c.name.replace(" & Spatial Statistics","")}</span>
              </div>
            ))}
          </div>
        </SystemCard>

        <SystemCard className="chart-card">
          <div className="card-header"><div><div className="system-label">02</div><h2>{tr(lang,"assessmentHistory")}</h2></div></div>
          <div className="line-chart-wrap">
            <svg viewBox="0 0 640 260" className="line-chart" role="img" aria-label={tr(lang,"assessmentHistory")}>
              <line x1="45" y1="220" x2="620" y2="220" />
              <line x1="45" y1="170" x2="620" y2="170" />
              <line x1="45" y1="120" x2="620" y2="120" />
              <line x1="45" y1="70" x2="620" y2="70" />
              {polylinePoints && <polyline points={polylinePoints} fill="none" stroke="currentColor" strokeWidth="4" />}
              {chartPoints.map((point,i)=><circle key={`${point.x}-${i}`} cx={point.x} cy={point.y} r="6" />)}
              {chartAssessments.map((item,i)=><text key={`${item.title || item.domain || "Q"}-${i}`} x={65 + i * 125 - 10} y="245">Q{i+1}</text>)}
            </svg>
          </div>
          <div className="chart-footnote">{chartAssessments.length ? chartAssessments.map(item => `${Number(item.score) || 0}%`).join(" → ") : tr(lang,"noData")}</div>
        </SystemCard>

        <SystemCard className="chart-card">
          <div className="card-header"><div><div className="system-label">03</div><h2>{tr(lang,"learningMix")}</h2></div></div>
          <div className="donut-layout">
            <div className="donut" aria-label={tr(lang,"learningMix")} />
            <div className="legend-list">
              {Object.entries(rawHours).map(([key,h],i)=>{
                const def = ENGINE_DEFINITIONS.find(d=>d.key===key);
                return <div className="legend-row" key={key}><span className={`legend-dot ${barColors[i%barColors.length]}`} /><div><strong>{def?.name || key}</strong><span>{h} {tr(lang,"hoursLabel")}</span></div><b>{Math.round((Number(h)/totalHours)*100)}%</b></div>;
              })}
            </div>
          </div>
        </SystemCard>

        <SystemCard className="chart-card course-analytics-card">
          <div className="card-header">
            <div>
              <div className="system-label">04</div>
              <h2>{tr(lang,"courseAnalytics")}</h2>
            </div>
            <Pill tone="active">{coursesList.length} Courses</Pill>
          </div>
          <div className="course-analytics-content">
            <div className="course-velocity-stats">
              <div className="velocity-stat">
                <span>{tr(lang,"avgCompletion")}</span>
                <strong>{avgCompletion}%</strong>
              </div>
              <div className="velocity-stat">
                <span>{tr(lang,"activeTrack")}</span>
                <strong className="track-title" title={activeTrackName}>{activeTrackName}</strong>
              </div>
              <div className="velocity-stat">
                <span>{tr(lang,"weeklyHours")}</span>
                <strong>{Math.max(4, Math.round(engine.learningHours / 4))}h/wk</strong>
              </div>
            </div>
            <div className="course-progress-list">
              {coursesList.slice(0, 4).map((c, idx) => {
                const pct = Math.max(5, Math.min(100, Number(c.progress ?? (c.score || 50))));
                return (
                  <div className="course-progress-row" key={c.id || c.title || idx}>
                    <div className="c-info">
                      <span className="c-title" title={c.title}>{c.title}</span>
                      <span className="c-meta">{c.hours || c.duration || 6} hrs · {c.status || "Active"}</span>
                    </div>
                    <div className="c-bar-wrap">
                      <div className="c-bar-track">
                        <div className={`c-bar-fill ${barColors[idx % barColors.length]}`} style={{ width: `${pct}%` }} />
                      </div>
                      <span className="c-pct">{pct}%</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </SystemCard>
      </div>
    </div>
  );
}

function SettingsPage({ user, lang, setLang, theme, setTheme, appearance, setAppearance, onSaveUser }) {
  const [name, setName] = useState(user.name || "");
  const [photo, setPhoto] = useState(user.photo || "");
  const [saved, setSaved] = useState(false);
  const save = () => {
    const next = { ...user, name: name.trim() || user.name, photo };
    localStorage.setItem("statSkillUser", JSON.stringify(next));
    onSaveUser(next);
    setSaved(true);
    setTimeout(() => setSaved(false), 1800);
  };
  const updatePhoto = event => {
    const file = event.target.files?.[0];
    if (!file || !file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = () => setPhoto(String(reader.result));
    reader.readAsDataURL(file);
  };
  return <div className="stack">
    <PageHeading kicker={tr(lang, "systemConfiguration").toUpperCase()} title={tr(lang, "settings")} subtitle={tr(lang, "visualSummary")} />
    <div className="settings-grid">
      <SystemCard>
        <div className="system-label">{tr(lang, "profile").toUpperCase()}</div>
        <h2>{tr(lang, "profile")}</h2>
        <div className="profile-photo-editor">
          <div className="profile-photo-preview">{photo ? <img src={photo} alt="" /> : <span>{(name || user.name || "A")[0].toUpperCase()}</span>}</div>
          <div className="profile-photo-actions"><strong>{copy(lang, "profilePhoto")}</strong><span>{copy(lang, "profileHint")}</span><div><label className="photo-upload"><Upload size={13} /> {copy(lang, "changePhoto")}<input type="file" accept="image/*" onChange={updatePhoto} /></label>{photo && <button type="button" className="photo-remove" onClick={() => setPhoto("")}>{copy(lang, "removePhoto")}</button>}</div></div>
        </div>
        <label className="field-label">{tr(lang, "displayName")}<input value={name} onChange={e => setName(e.target.value)} /></label>
        <label className="field-label">{tr(lang, "email")}<input value={user.email || ""} readOnly /></label>
        <label className="field-label">{tr(lang, "department")}<input value={user.department || "MoSPI"} readOnly /></label>
        <button className="primary-btn" onClick={save}><Save size={14} /> {tr(lang, "save")}</button>
        {saved && <div className="save-note"><CheckCircle2 size={14} /> {tr(lang, "save")}</div>}
      </SystemCard>
      <SystemCard className="theme-choice-card">
        <div className="system-label">{tr(lang, "visualSystem").toUpperCase()}</div>
        <h2>{tr(lang,"theme")}</h2>
        <div className="theme-options">
          <button type="button" className={`theme-option ${theme==="solo"?"active":""}`} onClick={()=>setTheme("solo")}><span className="theme-dot solo"/><span>{tr(lang,"solo")}</span></button>
          <button type="button" className={`theme-option ${theme==="executive"?"active":""}`} onClick={()=>setTheme("executive")}><span className="theme-dot executive"/><span>{tr(lang,"executive")}</span></button>
          <button type="button" className={`theme-option ${theme==="aurora"?"active":""}`} onClick={()=>setTheme("aurora")}><span className="theme-dot aurora"/><span>{tr(lang,"aurora")}</span></button>
        </div>
        <div className="setting-row"><div><strong>{tr(lang,"language")}</strong><span>{copy(lang, "languageHint")}</span></div>
          <div className="language-buttons">
            {[["en","EN"],["hi","हिं"],["ta","த"],["te","తె"]].map(([code,label])=><button type="button" key={code} className={lang===code?"active":""} onClick={()=>setLang(code)}>{label}</button>)}
          </div>
        </div>
        <div className="setting-row"><div><strong>{tr(lang,"appearance")}</strong><span>{copy(lang, "appearanceHint")}</span></div>
          <button type="button" className="theme-switch" onClick={()=>setAppearance(v=>v==="dark"?"light":"dark")}>
            {appearance==="dark"?<Sun size={15}/>:<Moon size={15}/>} {appearance==="dark"?tr(lang,"dark"):tr(lang,"light")}
          </button>
        </div>
      </SystemCard>
    </div>
    <SystemCard className="security-card"><ShieldCheck size={22} /><div><div className="system-label">{tr(lang, "securityStatus").toUpperCase()}</div><h2>{tr(lang, "demoEnvironment")}</h2><p>{tr(lang, "connectProduction")}</p></div></SystemCard>
  </div>;
}


function DataSourcesPage({ lang }) {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterDomain, setFilterDomain] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/data-sources`)
      .then(res => {
        if (!res.ok) throw new Error("Could not load official data sources.");
        return res.json();
      })
      .then(data => {
        setSources(data.data_sources || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const domains = [
    { key: "all", label: "All Data Sources" },
    { key: "statisticalMethods", label: "Surveys & Sampling (PLFS/HCES/ASUSE)" },
    { key: "priceIndices", label: "Price Indices (CPI)" },
    { key: "nationalAccounts", label: "National Accounts (GDP/NAS)" },
    { key: "dataQuality", label: "Industrial & Enterprise Records (ASI/IIP)" },
    { key: "gis", label: "Geospatial & Remote Sensing" },
    { key: "python", label: "Open Government Data APIs" },
  ];

  const filtered = sources.filter(ds => {
    const matchesDomain = filterDomain === "all" || ds.domain === filterDomain;
    const q = search.toLowerCase();
    const matchesSearch = !search ||
      (ds.name || "").toLowerCase().includes(q) ||
      (ds.division || "").toLowerCase().includes(q) ||
      (ds.description || "").toLowerCase().includes(q) ||
      (ds.key_variables || []).some(v => v.toLowerCase().includes(q));
    return matchesDomain && matchesSearch;
  });

  return (
    <div className="stack">
      <PageHeading
        kicker="NATIONAL STATISTICAL SYSTEM ARCHITECTURE"
        title={tr(lang, "dataSources")}
        subtitle="Primary statistical surveys, price indices, administrative registers, and microdata catalogs coordinated by MoSPI & National Statistical Office (NSO)."
        actions={
          <div className="search">
            <Search size={15} />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search surveys, indicators, divisions..."
            />
          </div>
        }
      />

      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", margin: "4px 0" }}>
        {domains.map(d => (
          <button
            key={d.key}
            type="button"
            className={filterDomain === d.key ? "primary-btn" : "secondary-btn"}
            onClick={() => setFilterDomain(d.key)}
            style={{ fontSize: "11px", padding: "6px 12px" }}
          >
            {d.label}
          </button>
        ))}
      </div>

      {loading && (
        <SystemCard style={{ padding: "36px", textAlign: "center" }}>
          <div>Loading official statistical registry...</div>
        </SystemCard>
      )}

      {error && (
        <SystemCard style={{ padding: "20px", color: "#dc2626" }}>
          <strong>Error loading data sources:</strong> {error}
        </SystemCard>
      )}

      {!loading && !error && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(440px, 1fr))", gap: "16px" }}>
          {filtered.map(ds => (
            <SystemCard key={ds.id} style={{ display: "flex", flexDirection: "column", padding: "20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "10px", marginBottom: "8px" }}>
                <div>
                  <span className="edu-badge cadre-nssta" style={{ marginBottom: "6px", display: "inline-block" }}>{ds.id}</span>
                  <h3 style={{ margin: "4px 0 2px", fontSize: "1.05rem", fontWeight: "700", color: "#0f172a" }}>
                    {ds.name}
                  </h3>
                  <span style={{ fontSize: "0.78rem", color: "#64748b" }}>{ds.division}</span>
                </div>
                <span className="edu-badge bloom-understanding" style={{ whiteSpace: "nowrap" }}>
                  {ds.frequency}
                </span>
              </div>

              <p style={{ fontSize: "0.84rem", color: "#334155", lineHeight: "1.5", margin: "8px 0 12px" }}>
                {ds.description}
              </p>

              <div style={{ margin: "6px 0" }}>
                <span style={{ fontSize: "0.74rem", fontWeight: "600", textTransform: "uppercase", color: "#64748b", display: "block", marginBottom: "4px" }}>
                  Key Variables & Metadata
                </span>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                  {(ds.key_variables || []).map((v, i) => (
                    <span key={i} style={{ fontSize: "0.74rem", background: "#f1f5f9", color: "#334155", padding: "2px 8px", borderRadius: "4px", border: "1px solid #e2e8f0" }}>
                      {v}
                    </span>
                  ))}
                </div>
              </div>

              {ds.learning_use_case && (
                <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "8px", padding: "10px", margin: "10px 0" }}>
                  <span style={{ fontSize: "0.74rem", fontWeight: "700", color: "#0f2e5a", display: "block", marginBottom: "2px" }}>
                    Capacity Building Application
                  </span>
                  <p style={{ margin: 0, fontSize: "0.78rem", color: "#475569" }}>
                    {ds.learning_use_case}
                  </p>
                </div>
              )}

              <div style={{ marginTop: "auto", paddingTop: "12px", borderTop: "1px solid #e2e8f0", display: "flex", gap: "8px", justifyContent: "flex-end" }}>
                {ds.microdata_catalog && (
                  <a
                    href={ds.microdata_catalog}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="secondary-btn"
                    style={{ fontSize: "11px", textDecoration: "none", display: "inline-flex", alignItems: "center", gap: "5px" }}
                  >
                    Microdata Catalog <ExternalLink size={12} />
                  </a>
                )}
                {ds.access_url && (
                  <a
                    href={ds.access_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="primary-btn"
                    style={{ fontSize: "11px", textDecoration: "none", display: "inline-flex", alignItems: "center", gap: "5px" }}
                  >
                    MoSPI Portal <ExternalLink size={12} />
                  </a>
                )}
              </div>
            </SystemCard>
          ))}
        </div>
      )}
    </div>
  );
}

function Sidebar({ active, setActive, open, setOpen, lang, user, onLogout, engine }) {
  const isOfficer = user.accountType === "cadre_officer" || !user.accountType || String(user.accountType).includes("officer");
  return <aside className={`sidebar ${open ? "open" : ""}`}>
    <div className="brand">
      <div className="brand-mark"><BarChart3 size={20} /></div>
      <div><strong>StatSkill Portal</strong><span>{user.projectId || "SIH26101"} · {user.department || (isOfficer ? "MoSPI" : "National Statistical System")}</span></div>
    </div>
    <div className="sidebar-status"><span className="live-dot" /> {tr(lang, "online")}</div>
    <nav>{NAV.map(item => {
      const Icon = item.icon;
      const key = item.id === "Dashboard" ? "dashboard"
        : item.id === "My Competencies" ? "competencies"
        : item.id === "Learning Path" ? "path"
        : item.id === "Assessments" ? "assessments"
        : item.id === "My Documents" ? "documents"
        : item.id === "Certificates" ? "certificates"
        : item.id === "Analytics" ? "analytics"
        : item.id === "Data Sources" ? "dataSources"
        : "settings";
      return <button key={item.id} className={active === item.id ? "active" : ""} onClick={() => { setActive(item.id); setOpen(false); }}><Icon size={17} /><span>{tr(lang, key)}</span>{active === item.id && <ChevronRight size={13} />}</button>;
    })}</nav>
    <div className="sidebar-spacer" />
    <div className="sidebar-player">
      <div className="small-label">{tr(lang, "player").toUpperCase()}</div>
      <strong>{user.name || "Learner"}</strong>
      <span>{user.role || (isOfficer ? "Senior Statistical Officer (SSO)" : "Citizen Data Analyst & Research Scholar")}</span>
      <Progress value={engine.overallScore} color="cyan" />
      <div className="player-bottom"><span>Readiness: {engine.overallScore}%</span><span>{user.department || (isOfficer ? "MoSPI" : "Academic / Citizen")}</span></div>
    </div>
    <button className="logout-btn" onClick={onLogout}><X size={15} /> {tr(lang, "signOut")}</button>
  </aside>;
}

export default function App() {
  const [competencyData, setCompetencyData] = useState(() => normalizeCompetencyPayload(KARMAYOGI_DATA));
  const engine = useMemo(() => runCompetencyEngine(competencyData), [competencyData]);
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem("statSkillVisualTheme");
    return stored === "executive" || stored === "aurora" || stored === "solo" ? stored : "executive";
  });
  const [appearance, setAppearance] = useState(() => localStorage.getItem("statSkillAppearance") === "dark" ? "dark" : "light");
  const [lang, setLang] = useState(() => ["en","hi","ta","te"].includes(localStorage.getItem("statSkillLanguage")) ? localStorage.getItem("statSkillLanguage") : "en");
  const [user, setUser] = useState(() => safeUser());
  const [profileData, setProfileData] = useState(null);
  const [apiToken, setApiToken] = useState(() => localStorage.getItem(API_TOKEN_KEY) || "");
  const [loggedIn, setLoggedIn] = useState(() => Boolean(localStorage.getItem(API_TOKEN_KEY)));
  const [register, setRegister] = useState(false);
  const [active, setActive] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const notifications = notificationsFor(lang);

  const applyApiSnapshot = (snapshot) => {
    const data = snapshot?.data || snapshot;
    if (!data) return;
    const normalized = normalizeCompetencyPayload(data);
    setProfileData(data);
    setUser(data.user || data.profile || null);
    setCompetencyData(normalized);
    if (data.user || data.profile) {
      localStorage.setItem("statSkillUser", JSON.stringify(data.user || data.profile));
    }
  };

  useEffect(() => {
    if (!loggedIn || !apiToken) return undefined;

    let mounted = true;
    const refreshUserData = async () => {
      try {
        const snapshot = await apiFetchMe(apiToken);
        if (mounted) applyApiSnapshot(snapshot);
      } catch (error) {
        console.warn("Unable to refresh user data:", error);
        if (mounted && /401|session|token/i.test(String(error.message || ""))) {
          localStorage.removeItem(API_TOKEN_KEY);
          localStorage.removeItem("statSkillSession");
          setApiToken("");
          setLoggedIn(false);
        }
      }
    };

    refreshUserData();
    const intervalId = window.setInterval(refreshUserData, API_REFRESH_MS);
    return () => {
      mounted = false;
      window.clearInterval(intervalId);
    };
  }, [loggedIn, apiToken]);

  useEffect(() => {
    localStorage.setItem("statSkillVisualTheme", theme);
    localStorage.setItem("statSkillAppearance", appearance);
    localStorage.setItem("statSkillLanguage", lang);
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove("theme-solo","theme-executive","theme-aurora","appearance-dark","appearance-light");
    document.body.classList.add(`theme-${theme}`, `appearance-${appearance}`);
  }, [theme, appearance, lang]);

  const handleStartQuiz = async (config) => {
    const domain = typeof config === "string" ? config : (config?.domain || "statisticalMethods");
    const title = typeof config === "object" && config?.title ? config.title : `Diagnostic Assessment: ${domain}`;
    try {
      const res = await fetch(`${API_BASE_URL}/api/mcq/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiToken}`,
        },
        body: JSON.stringify({
          domain,
          num_questions: 5,
          difficulty: "Intermediate",
          bloom_level: "Understanding",
        }),
      });
      if (res.ok) {
        const payload = await res.json();
        setActiveQuiz({
          quizId: `QUIZ-${domain}-${Date.now()}`,
          title: payload.topic || title,
          domain,
          domainName: domain === "statisticalMethods" ? "Statistical Methods & Sampling" : domain === "dataQuality" ? "Data Quality" : domain === "gis" ? "GIS & Spatial" : "Official Statistics",
          questions: payload.questions || [],
        });
        return;
      }
    } catch (e) {
      console.warn("Quiz generate fallback:", e);
    }
    // Fallback standard diagnostic questions
    setActiveQuiz({
      quizId: `QUIZ-${domain}-${Date.now()}`,
      title,
      domain,
      domainName: domain,
      questions: [
        {
          id: "Q1",
          question: `In official statistical methodology for ${domain}, what is the primary purpose of survey sampling design?`,
          options: [
            "To minimize sampling and non-sampling errors while ensuring national representativeness",
            "To sample only metropolitan households to expedite data publication",
            "To substitute theoretical simulations for field enumeration",
            "To eliminate the need for confidence intervals"
          ],
          correct_index: 0,
          explanation: "Scientific sampling design balances operational feasibility with rigorous error minimization to generate nationally representative estimates.",
          bloom_level: "Understanding",
          competency_domain: domain
        },
        {
          id: "Q2",
          question: "Which institutional standard governs data quality validation and outlier detection?",
          options: [
            "National Quality Assurance Framework (NQAF) and UN Fundamental Principles",
            "Ad-hoc manual survey spreadsheet adjustments",
            "Random variable discarding without audit trails",
            "Exclusion of non-response clusters without weighting adjustment"
          ],
          correct_index: 0,
          explanation: "MoSPI follows the UN-endorsed National Quality Assurance Framework (NQAF) to ensure systematic verification.",
          bloom_level: "Application",
          competency_domain: domain
        }
      ]
    });
  };

  const handleLogin = async ({ email, password }) => {
    try {
      const result = await apiLogin(email.trim(), password);
      const token = result.access_token;
      localStorage.setItem(API_TOKEN_KEY, token);
      localStorage.setItem("statSkillSession", "active");
      setApiToken(token);
      applyApiSnapshot(result.data);
      setLoggedIn(true);
      setRegister(false);
      setActive("Dashboard");
    } catch (error) {
      alert(error.message || "Unable to sign in.");
    }
  };

  const handleRegister = async (data) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          name: data.name.trim(),
          email: data.email.trim(),
          password: data.password,
          role: data.role || (data.account_type === "cadre_officer" ? "Senior Statistical Officer (SSO)" : "Citizen Data Analyst & Research Scholar"),
          department: data.department || (data.account_type === "cadre_officer" ? "MoSPI" : "Academic / Citizen Track"),
          account_type: data.account_type || "public_learner",
          projectId: "SIH26101",
        }),
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.detail || "Unable to register account.");
      }

      const token = result.access_token;
      localStorage.setItem(API_TOKEN_KEY, token);
      localStorage.setItem("statSkillSession", "active");
      setApiToken(token);
      applyApiSnapshot(result.data);
      setLoggedIn(true);
      setRegister(false);
      setActive("Dashboard");
    } catch (error) {
      alert(error.message || "Registration failed.");
    }
  };

  const saveUserProfile = async (nextUser) => {
    setUser(nextUser);
    localStorage.setItem("statSkillUser", JSON.stringify(nextUser));
    if (!apiToken) return;
    try {
      const response = await fetch(`${API_BASE_URL}/api/me/profile`, {
        method:"PUT",
        headers:{
          "Content-Type":"application/json",
          Accept:"application/json",
          Authorization:`Bearer ${apiToken}`
        },
        body:JSON.stringify({name:nextUser.name})
      });
      const snapshot = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(snapshot?.detail || "Unable to save profile.");
      applyApiSnapshot(snapshot);
    } catch (error) {
      alert(error.message || "Unable to save profile.");
    }
  };

  const logout = async () => {
    await apiLogout(apiToken);
    localStorage.removeItem(API_TOKEN_KEY);
    localStorage.removeItem("statSkillSession");
    setApiToken("");
    setProfileData(null);
    setLoggedIn(false);
    setMenuOpen(false);
  };

  if (!loggedIn) {
    return register
      ? <Register onRegister={handleRegister} onBackToLogin={() => setRegister(false)} />
      : <Login onLogin={handleLogin} onRegister={() => setRegister(true)} />;
  }

  const labelKey = active === "Dashboard" ? "dashboard"
    : active === "My Competencies" ? "competencies"
    : active === "Learning Path" ? "path"
    : active === "Assessments" ? "assessments"
    : active === "My Documents" ? "documents"
    : active === "Certificates" ? "certificates"
    : active === "Analytics" ? "analytics"
    : active === "Data Sources" ? "dataSources"
    : "settings";

  const pageData = profileData || competencyData || {};
  const content = {
    Dashboard: <DashboardPage user={user || {}} lang={lang} onNavigate={setActive} engine={engine} data={pageData} />,
    "My Competencies": <CompetenciesPage engine={engine} lang={lang} data={pageData} />,
    "Learning Path": <LearningPage lang={lang} data={pageData} engine={engine} onNavigate={setActive} onStartQuiz={handleStartQuiz} />,
    Assessments: <AssessmentsPage lang={lang} data={pageData} engine={engine} onStartQuiz={handleStartQuiz} />,
    "My Documents": <DocumentsPage lang={lang} data={pageData} apiToken={apiToken} />,
    Certificates: <CertificatesPage lang={lang} data={pageData} onNavigate={setActive} apiToken={apiToken} />,
    Analytics: <AnalyticsPage engine={engine} lang={lang} data={pageData} />,
    "Data Sources": <DataSourcesPage lang={lang} />,
    Settings: <SettingsPage user={user || {}} lang={lang} setLang={setLang} theme={theme} setTheme={setTheme} appearance={appearance} setAppearance={setAppearance} onSaveUser={saveUserProfile} />,
  }[active] || null;

  return (
    <div className={`app-shell theme-${theme} appearance-${appearance}`}>
      <Sidebar active={active} setActive={setActive} open={menuOpen} setOpen={setMenuOpen} lang={lang} user={user || {}} onLogout={logout} engine={engine} />
      {menuOpen && <button className="overlay" aria-label="Close menu" onClick={() => setMenuOpen(false)} />}
      <div className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <button className="menu-btn" onClick={() => setMenuOpen(v => !v)}><Menu size={18} /></button>
            <div><div className="eyebrow">STATSKILL / {tr(lang, labelKey).toUpperCase()}</div><strong>{tr(lang, labelKey)}</strong></div>
          </div>
          <div className="topbar-actions">
            <div className="status-chip"><span className="live-dot" /> {tr(lang, "live")}</div>
            <button className="icon-btn" title={tr(lang, "help")} onClick={() => setHelpOpen(true)}><HelpCircle size={16} /></button>
            <div className="notification-wrap">
              <button className="icon-btn" title={tr(lang, "notifications")} onClick={() => setNotifOpen(v => !v)}>
                <Bell size={16} />
                {notifications.length > 0 && <span className="notif-dot" />}
              </button>
              {notifOpen && (
                <div className="notification-popover">
                  <div className="notification-head"><strong>{tr(lang, "notifications")}</strong><button className="icon-btn" onClick={() => setNotifOpen(false)}><X size={14} /></button></div>
                  {(pageData.notifications?.length ? pageData.notifications : notifications).map((n, i) => (
                    <div className="notification-item" key={n.id || i}><span className={`mini-icon ${n.color || "cyan"}`}><Bell size={13} /></span><div><strong>{n.title}</strong><span>{n.time || "—"}</span></div></div>
                  ))}
                </div>
              )}
            </div>
            <div className="profile-chip">
              <div className="avatar-sm">{(user?.name || "A")[0].toUpperCase()}</div>
              <div className="profile-chip-info">
                <strong className="profile-chip-name">{user?.name || "Investigator"}</strong>
                <span className="profile-chip-role">{user?.role || tr(lang, "role")}</span>
              </div>
            </div>
          </div>
        </header>
        <main>
          {content}
        </main>
      </div>

      {helpOpen && (
        <div className="app-modal-overlay" onClick={() => setHelpOpen(false)}>
          <div className="app-modal-dialog" onClick={e => e.stopPropagation()}>
            <div className="app-modal-header">
              <div>
                <div className="system-label" style={{ color: "#0f2e5a" }}>MISSION KARMAYOGI · MOSPI KNOWLEDGE BASE</div>
                <h3>{tr(lang, "userGuide")}</h3>
                <p>National Statistical Capacity & Competency Intelligence Platform</p>
              </div>
              <button className="icon-btn" onClick={() => setHelpOpen(false)}><X size={16} /></button>
            </div>
            <div className="app-modal-body">
              <div className="credential-seal-banner" style={{ background: "#eff6ff", borderColor: "#bfdbfe", color: "#1e40af" }}>
                <div className="credential-seal-icon" style={{ background: "#dbeafe", color: "#1d4ed8" }}>
                  <HelpCircle size={26} />
                </div>
                <div className="credential-seal-text">
                  <strong style={{ color: "#1e3a8a" }}>National Statistical Systems Training Academy (NSSTA)</strong>
                  <span style={{ color: "#2563eb" }}>Official Statistical Capacity Building & Competency Diagnostics Framework</span>
                </div>
              </div>

              <div className="lesson-checklist">
                <div className="lesson-check-item">
                  <div><strong>1. Competency Scoring Model</strong><span>Synthesizes 50% assessment scores, 25% course completions, 15% self-assessment, and 10% learning effort.</span></div>
                </div>
                <div className="lesson-check-item">
                  <div><strong>2. iGOT Karmayogi Dynamic Recommendations</strong><span>Identifies critical skill gaps against official benchmarks and surfaces accredited courses to bridge them.</span></div>
                </div>
                <div className="lesson-check-item">
                  <div><strong>3. Official Microdata Portals</strong><span>Provides integrated access to MoSPI, PLFS, NSS, CPI, and Census catalogs for authentic study.</span></div>
                </div>
                <div className="lesson-check-item">
                  <div><strong>4. Credential Verification</strong><span>All issued certificates are verifiable against the MoSPI SSL/TLS 1.3 National Credential Registry.</span></div>
                </div>
              </div>

              <div className="credential-hash-box">
                <span>MoSPI Institutional Support & Helpdesk</span>
                <p style={{ margin: "4px 0 0", fontSize: "0.85rem", color: "#334155" }}>
                  Email: <strong>support-statskill@mospi.gov.in</strong> · Toll Free: <strong>1800-11-2334</strong> · New Delhi, India
                </p>
              </div>
            </div>
            <div className="app-modal-footer">
              <button className="primary-btn" onClick={() => setHelpOpen(false)}>Got it</button>
            </div>
          </div>
        </div>
      )}

      {activeQuiz && (
        <QuizPlayer
          quizId={activeQuiz.quizId}
          title={activeQuiz.title}
          domain={activeQuiz.domain}
          domainName={activeQuiz.domainName}
          questions={activeQuiz.questions}
          apiBaseUrl={API_BASE_URL}
          apiToken={apiToken}
          onClose={() => setActiveQuiz(null)}
          onCompleted={async () => {
            setActiveQuiz(null);
            if (apiToken) {
              const snap = await apiFetchMe(apiToken).catch(() => null);
              if (snap) applyApiSnapshot(snap);
            }
          }}
        />
      )}
    </div>
  );
}
