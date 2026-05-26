// ===== RGAIG+ Portal Data =====

const layers = [
  {n:1,name:'Consumer Wearable EEG Device',desc:'4-32 channel acquisition, electrode contact, signal quality monitoring',standards:'IEC 60601, ISO 13485',controls:'Electrical safety certification; quality management; electrode biocompatibility; SNR >= 10 dB',color:'var(--green)',textColor:'#fff'},
  {n:2,name:'Signal Processing Pipeline',desc:'Artifact removal, bandpass filtering, Fourier transform, epoch segmentation',standards:'ISO 14971',controls:'Risk management for signal artifacts; error propagation analysis; quality thresholds',color:'var(--green-light)',textColor:'#fff'},
  {n:3,name:'Diagnostic AI Models',desc:'CNN-LSTM, VotingClassifier, ensemble; MSCA 90.8%, 198 trained models',standards:'ISO/IEC 42001, FDA SaMD',controls:'AI model governance; predetermined change control; performance benchmarks',color:'var(--teal)',textColor:'#fff'},
  {n:4,name:'Generative AI Engine',desc:'RAG explanation, report generation, ChromaDB 1.4 GB, hallucination control',standards:'EU AI Act, OECD Principles',controls:'High-risk AI classification; transparency; hallucination control; faithfulness 0.92',color:'var(--navy-light)',textColor:'#fff'},
  {n:5,name:'Agentic Orchestration',desc:'NeuroMCP pipeline, multi-agent coordination, workflow automation',standards:'NIST AI RMF',controls:'Risk mapping for autonomous decisions; human-in-the-loop; audit logging',color:'var(--navy)',textColor:'#fff'},
  {n:6,name:'Consumer Interface',desc:'Dashboard, alerts, consultation prompts, medical disclaimers, confidence scores',standards:'IEC 62366-1, ISO 9241-210',controls:'Usability engineering; human-centred design; accessibility compliance',color:'var(--gold-dark)',textColor:'#fff'},
  {n:7,name:'Clinical Oversight',desc:'Clinician validation, escalation pathway, expert consultation, human-in-the-loop',standards:'IMDRF SaMD, WHO AI Health',controls:'Clinical validation; clinician-in-the-loop for high-risk; informed consent',color:'var(--maroon)',textColor:'#fff'},
  {n:8,name:'Continuous Monitoring',desc:'Drift detection, safety alerts, fairness tracking, trust metrics, device health',standards:'ISO/IEC 27001, IEEE 7000',controls:'Information security; ethical surveillance; drift detection; bias monitoring',color:'var(--maroon-light)',textColor:'#fff'},
  {n:9,name:'Governance & Compliance',desc:'525-module taxonomy, audit trail, regulatory alignment (EU AI Act, FDA SaMD)',standards:'HIPAA, GDPR, ISO/IEC 42001',controls:'Data privacy; cross-jurisdictional governance; audit trails; regulatory reporting',color:'var(--maroon-dark)',textColor:'#fff'}
];

const pillars = [
  {name:'Responsible AI',icon:'fa-shield-halved',rate:'98.4%',color:'var(--navy)',
   desc:'Fairness, accountability, transparency across all layers.',
   details:'Bias detection (disparate impact ratio), fairness metrics (demographic parity, equalized odds), accountability chains, transparency reports, ethical review board oversight.',
   questions:['Is bias testing performed before deployment?','Are fairness metrics (demographic parity, equalized odds) tracked?','Is there an accountability chain for AI decisions?','Are transparency reports generated for stakeholders?','Is there a process for reporting AI discrimination?'],
   tools:['IBM AI Fairness 360','Google What-If Tool','SHAP fairness analysis','Aequitas bias audit','Custom fairness dashboard'],
   challenges:['Defining "fair" across diverse populations','Historical bias in training data','Intersectional bias detection','Balancing accuracy vs fairness trade-offs'],
   edgeCases:['Underrepresented demographic groups in EEG data','Cultural differences in disease presentation','Age-related signal variations','Gender-imbalanced datasets'],
   solutions:['Stratified sampling across demographics','Adversarial debiasing during training','Regular bias audits (quarterly)','External ethics board review'],
   planning:['Phase 1: Bias baseline assessment','Phase 2: Fairness metric integration','Phase 3: Automated bias monitoring','Phase 4: External audit certification']},
  {name:'Governance AI',icon:'fa-landmark',rate:'98.4%',color:'var(--maroon)',
   desc:'Policy enforcement, audit trails, compliance automation, decision engine.',
   details:'525-module taxonomy compliance, automated audit trails, governance board structure, policy versioning, regulatory alignment (15 standards), decision engine with escalation.',
   questions:['Is there a formal AI governance board?','Are AI policies documented and versioned?','Is there an automated compliance checking engine?','Are audit trails maintained for all AI decisions?','Is there a regulatory alignment matrix?'],
   tools:['Custom governance dashboard','Policy versioning system','Automated compliance checker','Audit trail database','Regulatory mapping tool'],
   challenges:['Keeping policies current with evolving regulations','Cross-jurisdictional compliance (EU/US/APAC)','Balancing governance overhead vs agility','Measuring governance effectiveness'],
   edgeCases:['Model decisions in regulatory gray areas','Cross-border data governance conflicts','Emergency override scenarios','Governance for edge-deployed models'],
   solutions:['525-module taxonomy with automated checks','4-level risk scoring with escalation','Quarterly governance review cycles','Regulatory change monitoring service'],
   planning:['Phase 1: Governance board formation','Phase 2: Policy documentation','Phase 3: Automated compliance engine','Phase 4: Continuous governance monitoring']},
  {name:'Risk AI',icon:'fa-triangle-exclamation',rate:'97.8%',color:'var(--green)',
   desc:'Risk identification, assessment, mitigation with 4-level matrix.',
   details:'Risk taxonomy (clinical, technical, operational, regulatory), 4-level scoring, automated escalation, sensitivity analysis (3-scenario + tornado).',
   questions:['Is there a formal AI risk taxonomy?','Are risks scored on likelihood and impact?','Is there automated risk escalation?','Are sensitivity analyses performed regularly?','Is there a risk mitigation plan for each category?'],
   tools:['Risk scoring engine','Sensitivity analysis toolkit','Monte Carlo simulation','Tornado diagram generator','Risk dashboard with alerts'],
   challenges:['Quantifying clinical risk from AI errors','Unknown unknowns in novel disease patterns','Cascading risk across 9 layers','Real-time risk assessment at inference'],
   edgeCases:['Model confidence just above/below threshold','Contradictory signals from multi-agent system','Device malfunction during active diagnosis','Rare disease variants not in training data'],
   solutions:['4-level risk matrix (Low/Medium/High/Critical)','Automated escalation to human clinician','3-scenario sensitivity analysis','Tornado diagram for parameter sensitivity'],
   planning:['Phase 1: Risk taxonomy development','Phase 2: Scoring engine deployment','Phase 3: Automated escalation rules','Phase 4: Continuous risk monitoring']},
  {name:'Ethical AI',icon:'fa-scale-balanced',rate:'98.1%',color:'var(--teal)',
   desc:'Ethics review, informed consent, privacy, vulnerable populations.',
   details:'IRB compliance, informed consent protocols, HIPAA/GDPR data protection, vulnerable population safeguards, ethics review board, cultural sensitivity assessment.',
   questions:['Is IRB approval obtained for all data use?','Is informed consent documented for all participants?','Are HIPAA/GDPR protections implemented?','Are vulnerable populations given extra safeguards?','Is there an ethics review process for new features?'],
   tools:['IRB compliance tracker','Consent management platform','HIPAA compliance scanner','GDPR data mapping tool','Ethics review workflow'],
   challenges:['Consent for secondary use of public datasets','Privacy vs model accuracy trade-off','Cultural sensitivity in global deployment','Vulnerable population identification'],
   edgeCases:['Pediatric patients (ASD) requiring guardian consent','Mental health stigma in certain cultures','Data from deceased subjects','Cross-cultural interpretation of diagnosis'],
   solutions:['Multi-layer consent framework','De-identification verification pipeline','Cultural advisory board','Vulnerability assessment protocol'],
   planning:['Phase 1: Ethics framework design','Phase 2: Consent management system','Phase 3: Privacy impact assessment','Phase 4: External ethics audit']},
  {name:'Performance AI',icon:'fa-chart-line',rate:'97.4%',color:'var(--navy-light)',
   desc:'Accuracy optimization, throughput, latency across 5 domains.',
   details:'k-fold CV (k=10), LOSO validation, bootstrap CI (1000 resamples), ablation study, hyperparameter optimization, inference latency < 100ms.',
   questions:['Are performance benchmarks defined for each disease?','Is cross-validation (k-fold, LOSO) systematic?','Are confidence intervals reported for all metrics?','Is inference latency measured and optimized?','Are ablation studies conducted for each component?'],
   tools:['MLflow experiment tracking','Optuna hyperparameter optimization','Bootstrap CI calculator','Latency profiler','Ablation study framework'],
   challenges:['Maintaining accuracy across diverse populations','Balancing model complexity vs inference speed','Handling class imbalance in rare diseases','Generalizing across different EEG hardware'],
   edgeCases:['Patient with multiple comorbid conditions','Extremely noisy EEG signal','Edge device with limited compute','Real-time seizure detection requirements'],
   solutions:['Ensemble methods for robust accuracy','Model compression for edge deployment','SMOTE/class weighting for imbalance','Hardware-specific optimization profiles'],
   planning:['Phase 1: Baseline benchmarking','Phase 2: Optimization pipeline','Phase 3: Edge deployment profiling','Phase 4: Continuous performance monitoring']},
  {name:'Explainable AI',icon:'fa-lightbulb',rate:'98.2%',color:'var(--gold-dark)',
   desc:'SHAP, RAG explanations, feature importance, plain-language outputs.',
   details:'SHAP feature importance, attention visualization, RAG-generated clinical narratives, faithfulness 0.92, context precision 0.94.',
   questions:['Are SHAP values computed for every prediction?','Are RAG explanations validated for faithfulness?','Are consumer-friendly explanations generated?','Are clinician-detailed reports available?','Is explanation quality monitored over time?'],
   tools:['SHAP library','RAGAS evaluation framework','Attention visualization toolkit','Plain-language generator','Explanation quality dashboard'],
   challenges:['Making complex ML decisions understandable','Ensuring RAG explanations are faithful','Balancing detail vs simplicity','Multi-language explanation support'],
   edgeCases:['Model disagrees with RAG explanation','Explanation for borderline predictions','Consumer misinterprets confidence score','Clinician disagrees with AI reasoning'],
   solutions:['Dual-track explanations (consumer + clinician)','Faithfulness threshold (>0.90) enforcement','Confidence calibration with verbal labels','Human review for high-risk explanations'],
   planning:['Phase 1: SHAP integration','Phase 2: RAG explanation pipeline','Phase 3: Consumer language templates','Phase 4: Explanation quality monitoring']},
  {name:'Interpretable AI',icon:'fa-magnifying-glass-chart',rate:'97.9%',color:'var(--maroon-light)',
   desc:'Model transparency, decision paths, feature attribution.',
   details:'Decision tree surrogates, attention heatmaps, feature contribution plots, prediction confidence intervals, model card documentation.',
   questions:['Are model cards maintained for all deployed models?','Are decision paths traceable for any prediction?','Are feature contribution plots available?','Are confidence intervals displayed with predictions?','Is model behavior documented for edge cases?'],
   tools:['Model card generator','LIME local explanations','Attention heatmap renderer','Confidence interval calculator','Decision path tracer'],
   challenges:['Deep learning models inherently opaque','Trade-off between interpretability and accuracy','Explaining ensemble decisions','Temporal feature interpretation in EEG'],
   edgeCases:['Prediction based on single dominant feature','Model uses artifact as discriminative feature','Attention focuses on unexpected brain region','Ensemble members disagree significantly'],
   solutions:['Surrogate model approximation','Attention map validation against neuroscience','Feature sanity checks','Ensemble disagreement flagging'],
   planning:['Phase 1: Model card creation','Phase 2: Surrogate model training','Phase 3: Attention validation pipeline','Phase 4: Interpretability dashboard']},
  {name:'Portable AI',icon:'fa-arrows-rotate',rate:'98.0%',color:'var(--green-light)',
   desc:'Cross-domain generalization, multi-disease, edge deployment.',
   details:'5 disease domains validated, transfer learning, ONNX export, edge models (< 500MB), cross-platform (iOS/Android/Web).',
   questions:['Can models generalize across disease domains?','Is transfer learning validated between datasets?','Are models exportable to edge devices?','Is cross-platform deployment supported?','Are models tested on different EEG hardware?'],
   tools:['ONNX Runtime','TensorFlow Lite','Transfer learning toolkit','Cross-platform test suite','Hardware compatibility matrix'],
   challenges:['Domain shift between datasets','Hardware-specific signal characteristics','Model size constraints on mobile','Offline mode data handling'],
   edgeCases:['New EEG device with different channel layout','Diagnosis request with no internet connectivity','Model update while patient session active','Cross-cultural EEG pattern differences'],
   solutions:['Domain adaptation layers','Hardware abstraction preprocessing','Progressive model loading','Graceful offline fallback'],
   planning:['Phase 1: ONNX export pipeline','Phase 2: Edge optimization','Phase 3: Cross-platform testing','Phase 4: Hardware compatibility certification']},
  {name:'Energy-Efficient AI',icon:'fa-leaf',rate:'100%',color:'var(--success)',
   desc:'Green AI, compute optimization, carbon footprint tracking.',
   details:'Model pruning (30%), quantization (INT8), knowledge distillation, batch optimization, carbon tracking.',
   questions:['Is model inference energy consumption measured?','Are models pruned/quantized for efficiency?','Is carbon footprint tracked per prediction?','Are batch processing strategies implemented?','Is green hosting used for cloud deployment?'],
   tools:['CodeCarbon tracker','Neural network pruning toolkit','INT8 quantization tools','Batch inference optimizer','Green cloud provider selector'],
   challenges:['Accuracy loss from aggressive compression','Real-time inference energy constraints','Measuring embedded device power usage','Carbon accounting across full pipeline'],
   edgeCases:['Battery-constrained wearable device','High-frequency continuous monitoring mode','Large batch processing during peak hours','Model retraining energy budget exceeded'],
   solutions:['Pareto-optimal accuracy-efficiency frontier','Adaptive inference (light model for screening, full for diagnosis)','Off-peak batch scheduling','Carbon budget allocation per model'],
   planning:['Phase 1: Energy baseline measurement','Phase 2: Model compression','Phase 3: Carbon tracking dashboard','Phase 4: Green certification']},
  {name:'Secure AI',icon:'fa-lock',rate:'98.5%',color:'var(--gray-800)',
   desc:'Encryption, access control, adversarial defense, PII protection.',
   details:'AES-256 at rest, TLS 1.3 in transit, RBAC, adversarial robustness, PII masking, differential privacy.',
   questions:['Is data encrypted at rest and in transit?','Is role-based access control implemented?','Are adversarial robustness tests performed?','Is PII detected and masked automatically?','Is there an incident response plan for breaches?'],
   tools:['AES-256 encryption engine','RBAC management system','Adversarial attack simulator','PII detection scanner','Security incident response toolkit'],
   challenges:['Adversarial attacks on EEG signals','PII leakage through model inversion','Secure model serving at edge','Key management across distributed system'],
   edgeCases:['Adversarial perturbation mimicking disease pattern','Model extraction via repeated API queries','Device compromise during patient session','Cross-tenant data leakage in cloud'],
   solutions:['Adversarial training and input validation','Rate limiting and query monitoring','Secure enclave for edge inference','Tenant isolation with encryption boundaries'],
   planning:['Phase 1: Security architecture design','Phase 2: Encryption and RBAC deployment','Phase 3: Adversarial testing','Phase 4: Security audit and certification']}
];

const diseases = [
  {name:'Autism (ASD)',acc:'97.67%',f1:'0.976',auc:'0.983',subjects:316,impact:'1 in 36 children (CDC)',color:'#1f77b4',channels:19,
   papers:['Bosl et al. (2018) EEG analytics for ASD','Dickinson et al. (2021) EEG biomarkers in ASD','Kang et al. (2020) Deep learning EEG classification'],
   eegPattern:'Atypical gamma power, reduced alpha coherence, frontal-posterior connectivity differences'},
  {name:"Parkinson's (PD)",acc:'100.0%',f1:'1.000',auc:'1.000',subjects:64,impact:'10M worldwide',color:'#ff7f0e',channels:14,
   papers:['Anjum et al. (2020) EEG-based PD diagnosis','Oh et al. (2020) Deep CNN for PD detection','Khare et al. (2021) Automated PD EEG analysis'],
   eegPattern:'Excessive beta in motor cortex, reduced theta/alpha ratio, slowed background activity'},
  {name:'Epilepsy',acc:'99.02%',f1:'0.990',auc:'0.992',subjects:118,impact:'50M worldwide',color:'#2ca02c',channels:32,
   papers:['Andrzejak et al. (2001) Bonn EEG dataset','Acharya et al. (2018) Deep learning seizure detection','Shoeibi et al. (2021) Epileptic seizure DL review'],
   eegPattern:'Spike-and-wave complexes, focal/generalized seizure patterns, interictal discharges'},
  {name:'Stress',acc:'94.17%',f1:'0.940',auc:'0.953',subjects:140,impact:'77% experience stress',color:'#d62728',channels:14,
   papers:['Schmidt et al. (2018) WESAD dataset','Giannakakis et al. (2019) EEG stress detection','Al-Shargie et al. (2019) Mental stress EEG'],
   eegPattern:'Elevated frontal beta, reduced alpha asymmetry, increased theta-beta ratio'},
  {name:'Depression',acc:'91.07%',f1:'0.908',auc:'0.926',subjects:130,impact:'280M globally',color:'#9467bd',channels:32,
   papers:['Mumtaz et al. (2017) EEG-based MDD classification','Acharya et al. (2018) Automated depression EEG','Cai et al. (2020) Deep learning MDD EEG diagnosis'],
   eegPattern:'Frontal alpha asymmetry (left < right), increased theta power, reduced prefrontal connectivity'}
];

const channelConfigs = [
  {ch:4,name:'Emotiv Insight',grade:'Consumer',positions:'AF3, AF4, T7, T8, Pz(ref)',resolution:'Low',useCase:'Basic wellness, meditation, attention tracking',accuracy:'85-90%',cost:'$300-400',diseases:['Stress'],color:'var(--green-light)'},
  {ch:8,name:'Basic Research',grade:'Consumer+',positions:'Fp1, Fp2, C3, C4, P3, P4, O1, O2',resolution:'Low-Medium',useCase:'Research screening, BCI applications, basic diagnosis',accuracy:'88-93%',cost:'$500-800',diseases:['Stress','Depression'],color:'var(--green)'},
  {ch:14,name:'Emotiv EPOC X',grade:'Research',positions:'AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4',resolution:'Medium',useCase:'Research-grade diagnosis, multi-domain screening, PD detection',accuracy:'92-97%',cost:'$800-1200',diseases:['PD','Stress','ASD'],color:'var(--teal)'},
  {ch:16,name:'g.tec/OpenBCI',grade:'Research+',positions:'10-20 subset + extended',resolution:'Medium-High',useCase:'Advanced research, seizure monitoring, connectivity analysis',accuracy:'94-98%',cost:'$1500-3000',diseases:['Epilepsy','PD','Stress'],color:'var(--navy-light)'},
  {ch:24,name:'BioSemi/ANT',grade:'Clinical-',positions:'Extended 10-20 with temporal chains',resolution:'High',useCase:'Clinical research, source localization, complex diagnosis',accuracy:'96-99%',cost:'$5000-15000',diseases:['Epilepsy','ASD','Depression'],color:'var(--navy)'},
  {ch:32,name:'Clinical EEG',grade:'Clinical',positions:'Full 10-20 + 10-10 extensions',resolution:'Very High',useCase:'Full clinical diagnosis, epilepsy monitoring, depression assessment',accuracy:'97-100%',cost:'$15000-50000',diseases:['All 5 diseases'],color:'var(--maroon)'}
];

const industries = [
  {name:'Healthcare',icon:'fa-hospital',bg:'var(--maroon)',maturity:'Level 5',items:['EEG-based neurological diagnosis','Clinical AI decision support','Patient safety governance','Wearable device monitoring','GenAI diagnostic explanations','HIPAA/FDA compliance']},
  {name:'Banking & Finance',icon:'fa-building-columns',bg:'var(--navy)',maturity:'Level 4',items:['Fraud detection AI governance','Credit scoring fairness','Regulatory compliance (Basel III)','Algorithmic trading oversight','Customer risk profiling','PII protection & encryption']},
  {name:'Oil & Gas',icon:'fa-oil-well',bg:'var(--green-dark)',maturity:'Level 3',items:['Predictive maintenance AI','Safety incident monitoring','Environmental compliance AI','Pipeline anomaly detection','Worker safety wearables','IoT sensor governance']},
  {name:'Logistics',icon:'fa-truck-fast',bg:'var(--teal)',maturity:'Level 3',items:['Supply chain AI governance','Demand forecasting transparency','Autonomous vehicle oversight','Route optimization fairness','Warehouse robotics safety','Real-time tracking AI']}
];

const compHeaders = ['Capability','NIST AI RMF','ISO 42001','EU AI Act','RAISEF','RGAIG+'];
const compCaps = [
  ['Responsible AI governance','check','check','check','check','check'],
  ['Risk management framework','check','check','check','partial','check'],
  ['Operational monitoring','partial','partial','dash','partial','check'],
  ['Generative AI governance','dash','dash','partial','dash','check'],
  ['Wearable device integration','dash','dash','dash','dash','check'],
  ['Consumer trust & adoption','dash','dash','dash','partial','check'],
  ['GenAI decision engine','dash','dash','dash','dash','check'],
  ['Continuous drift detection','partial','partial','dash','partial','check'],
  ['Structured evaluation','dash','dash','dash','dash','check'],
  ['Maturity model pathway','dash','dash','dash','dash','check'],
  ['Multi-domain biomedical AI','dash','dash','dash','dash','check'],
  ['525-module taxonomy','dash','dash','dash','dash','check'],
  ['Agentic AI governance','dash','dash','dash','dash','check'],
  ['RAG faithfulness controls','dash','dash','dash','dash','check'],
  ['Device-to-diagnosis governance','dash','dash','dash','dash','check']
];

const phases = [
  {n:1,name:'Topic Selection',ch:'Ch.1',output:'Research problem defined'},
  {n:2,name:'Literature Review',ch:'Ch.2',output:'120+ sources synthesized'},
  {n:3,name:'Conceptual Model',ch:'Ch.2',output:'6-construct model'},
  {n:4,name:'Hypothesis Development',ch:'Ch.2',output:'H1-H5 formulated'},
  {n:5,name:'Research Design',ch:'Ch.3',output:'Mixed methods design'},
  {n:6,name:'Measurement Design',ch:'Ch.3',output:'57 survey items'},
  {n:7,name:'Sampling Strategy',ch:'Ch.3',output:'768+ subjects'},
  {n:8,name:'Data Collection',ch:'Ch.3',output:'305 GB collected'},
  {n:9,name:'Data Preparation',ch:'Ch.4',output:'Clean datasets'},
  {n:10,name:'Statistical Analysis',ch:'Ch.4',output:'H1-H5 tested'},
  {n:11,name:'Results Interpretation',ch:'Ch.5',output:'All hypotheses supported'},
  {n:12,name:'Contributions',ch:'Ch.5',output:'C1-C8 contributions'},
  {n:13,name:'Thesis Writing',ch:'Cross',output:'562 pages'},
  {n:14,name:'Quality Validation',ch:'Cross',output:'525 modules passed'},
  {n:15,name:'Defense Preparation',ch:'Post',output:'60 Q&A prepared'}
];

const lifecycleData = [
  {icon:'fa-database',title:'INPUT',desc:'EEG signals, clinical datasets, 305 GB raw data, 768+ subjects across 5 disease domains'},
  {icon:'fa-gears',title:'PROCESS',desc:'ML/DL pipeline: preprocessing, Fourier transform, feature extraction, model training, RAG generation'},
  {icon:'fa-file-medical',title:'OUTPUT',desc:'Diagnostic predictions, confidence scores, plain-language explanations, clinical reports'},
  {icon:'fa-microscope',title:'EVALUATION',desc:'k-fold CV, LOSO, bootstrap CI, ablation study, RAGAS metrics, expert panel assessment'},
  {icon:'fa-satellite-dish',title:'MONITORING',desc:'Model drift (PSI/CSI), data drift, bias surveillance, trust metrics, device health, safety alerts'},
  {icon:'fa-ranking-star',title:'BENCHMARKING',desc:'MSCA 90.8%, AUC 0.956, 15 standards compliance, 525-module pass rate, framework comparison'}
];

const expertItems = [
  {id:'EP-1',text:'The RGAIG framework provides a comprehensive approach to multi-domain biomedical AI diagnosis'},
  {id:'EP-2',text:'The 9-layer architecture addresses real clinical workflow requirements'},
  {id:'EP-3',text:'The 525-module quality taxonomy covers all critical AI governance dimensions'},
  {id:'EP-4',text:'The diagnostic accuracy results (MSCA 90.8%) meet clinical deployment thresholds'},
  {id:'EP-5',text:'The framework offers novel capabilities not available in existing AI diagnostic systems'},
  {id:'EP-6',text:'The cross-domain results demonstrate generalisable diagnostic capability'},
  {id:'EP-7',text:'The deep learning models show meaningful improvement over classical ML baselines'},
  {id:'EP-8',text:'The SHAP-identified top features are clinically meaningful'},
  {id:'EP-9',text:'The bootstrap CIs and LOSO results provide sufficient evidence of robustness'},
  {id:'EP-10',text:'The agentic orchestration reduces manual diagnostic workflow steps'},
  {id:'EP-11',text:'The RAG-generated explanations are accurate and clinically trustworthy'},
  {id:'EP-12',text:'The RAG outputs faithfully represent predictions without hallucination'},
  {id:'EP-13',text:'The 10-pillar governance addresses all critical responsible AI requirements'},
  {id:'EP-14',text:'The framework is compatible with EU AI Act and FDA SaMD requirements'},
  {id:'EP-15',text:'The governance provides sufficient audit trail for regulatory inspection'}
];

const tamItems = [
  {id:'PU-1',text:'Using RGAIG would improve diagnostic accuracy in clinical practice'},
  {id:'PU-2',text:'Multi-domain capability would reduce need for separate diagnostic tools'},
  {id:'PU-3',text:'RAG explanations would help communicate findings to patients'},
  {id:'PU-4',text:'Governance audit trail would simplify regulatory compliance'},
  {id:'PE-1',text:'Agentic pipeline would be easy to integrate into clinical workflows'},
  {id:'PE-2',text:'Learning to use RGAIG would not require extensive technical training'},
  {id:'PE-3',text:'Diagnostic output format would be easy to interpret'},
  {id:'BI-1',text:'I would intend to use RGAIG in clinical practice if available'},
  {id:'BI-2',text:'I would recommend RGAIG to colleagues'},
  {id:'TC-1',text:'ML/DL technology is mature enough for clinical deployment'},
  {id:'TC-2',text:'EEG signal processing pipeline is technically sound'},
  {id:'TC-3',text:'RAG retrieval provides reliable medical knowledge'},
  {id:'OC-1',text:'My organisation has IT infrastructure to support RGAIG'},
  {id:'OC-2',text:'My organisation has staff with sufficient AI literacy'},
  {id:'OC-3',text:'Management would support AI-assisted diagnostic adoption'},
  {id:'EC-1',text:'Regulatory requirements create pressure to adopt governed AI'},
  {id:'EC-2',text:'Competitive pressure incentivises AI adoption'},
  {id:'EC-3',text:'Patient expectations drive AI adoption'},
  {id:'RV-1',text:'RGAIG creates measurable clinical and economic value'},
  {id:'RV-2',text:'No comparable framework exists in the market'},
  {id:'RV-3',text:'The 525-module taxonomy would be difficult to replicate'},
  {id:'RV-4',text:'No alternative provides equivalent governed AI diagnostics'}
];

const trustItems = [
  {id:'TT-1',text:'I trust the diagnostic accuracy (MSCA 90.8%) for clinical decision-making'},
  {id:'TT-2',text:'I trust consistent results across repeated evaluations'},
  {id:'TT-3',text:'I trust the framework to flag uncertain predictions'},
  {id:'TT-4',text:'I trust a single framework across multiple disease domains'},
  {id:'CT-1',text:'RAG explanations provide sufficient clinical reasoning'},
  {id:'CT-2',text:'Clinicians retain final decision authority'},
  {id:'CT-3',text:'Safety mechanisms prevent harm'},
  {id:'CT-4',text:'Framework provides adequate informed consent information'},
  {id:'OT-1',text:'Governance maintains complete audit trail'},
  {id:'OT-2',text:'Fairness metrics detect demographic bias'},
  {id:'OT-3',text:'Data protection controls protect patient privacy'},
  {id:'OT-4',text:'10-pillar taxonomy meets regulatory requirements'}
];

const isoNistComparison = [
  {dim:'Scope','iso':'AI Management System (AIMS)','nist':'AI Risk Management','rgaig':'Unified AI Governance + Clinical Deployment'},
  {dim:'Risk Approach','iso':'ISO 31000 risk-based','nist':'4 functions: Govern, Map, Measure, Manage','rgaig':'9-layer + 4-level risk scoring + automated escalation'},
  {dim:'GenAI Coverage','iso':'Limited (Annex)','nist':'NIST AI 600-1 (separate doc)','rgaig':'Native: RAG, hallucination, faithfulness, agentic'},
  {dim:'Healthcare Focus','iso':'Generic (any industry)','nist':'Generic (any industry)','rgaig':'Purpose-built: EEG, wearables, clinical workflows'},
  {dim:'Device Governance','iso':'Not covered','nist':'Not covered','rgaig':'Layer 1: IEC 60601, ISO 13485, 8-dim benchmark'},
  {dim:'Trust Model','iso':'Implied','nist':'Trustworthy AI principles','rgaig':'TAM-TOE-RBV with SEM validation (H1-H5)'},
  {dim:'Validation','iso':'Certification audit','nist':'Self-assessment profiles','rgaig':'525-module taxonomy, 97.4-98.4% pass rates'},
  {dim:'Explainability','iso':'Required but not specified','nist':'Principles only','rgaig':'SHAP + RAG (faithfulness 0.92, precision 0.94)'},
  {dim:'Monitoring','iso':'Continual improvement','nist':'Measure function','rgaig':'Real-time: PSI/CSI drift, bias, safety, device health'},
  {dim:'Maturity Model','iso':'PDCA cycle','nist':'Tiered profiles','rgaig':'5-level CMM with KPI thresholds per level'}
];

const mlopsStages = [
  {name:'Data Versioning',icon:'fa-code-branch',desc:'DVC-tracked datasets, 305 GB versioned, reproducible pipelines',color:'var(--green)'},
  {name:'Feature Store',icon:'fa-warehouse',desc:'Centralized features: spectral, temporal, connectivity, nonlinear (200+ features per subject)',color:'var(--green-light)'},
  {name:'Experiment Tracking',icon:'fa-flask',desc:'MLflow experiment logging, hyperparameter tracking, metric comparison across 198 models',color:'var(--teal)'},
  {name:'Model Registry',icon:'fa-box-archive',desc:'Versioned models (joblib), metadata (dataset hash, hyperparams, metrics), approval workflow',color:'var(--navy-light)'},
  {name:'CI/CD Pipeline',icon:'fa-arrows-spin',desc:'Automated training, validation, testing; triggered by data or code changes',color:'var(--navy)'},
  {name:'Model Serving',icon:'fa-server',desc:'REST API inference, batch processing, edge deployment (ONNX), < 100ms latency',color:'var(--maroon)'},
  {name:'Monitoring',icon:'fa-chart-line',desc:'PSI/CSI drift detection, accuracy degradation alerts, bias monitoring, auto-retraining triggers',color:'var(--maroon-light)'},
  {name:'Governance',icon:'fa-shield-halved',desc:'Audit trail, model cards, fairness reports, regulatory documentation, approval gates',color:'var(--gold-dark)'}
];

const llmopsStages = [
  {name:'Knowledge Ingestion',icon:'fa-book-open',desc:'Medical literature, clinical guidelines, drug databases. Recursive chunking (512 tokens, 50 overlap)',color:'var(--maroon)'},
  {name:'Embedding Pipeline',icon:'fa-vector-square',desc:'Sentence transformers (768-dim), ChromaDB vector store (1.4 GB), batch embedding updates',color:'var(--maroon-light)'},
  {name:'Prompt Engineering',icon:'fa-pen-nib',desc:'Disease-specific templates, chain-of-thought reasoning, safety guardrails, clinical context injection',color:'var(--navy)'},
  {name:'RAG Orchestration',icon:'fa-diagram-project',desc:'Query expansion, hypothesis-aware retrieval, re-ranking, top-k=5 context, citation validation',color:'var(--navy-light)'},
  {name:'Model Selection',icon:'fa-brain',desc:'Task routing: Vision (EEG maps) | Text (explanations) | Multimodal (combined) | SLM (edge)',color:'var(--teal)'},
  {name:'Output Evaluation',icon:'fa-check-double',desc:'RAGAS: Faithfulness 0.92, Relevance 0.89, Precision 0.94. Hallucination detection + citation check',color:'var(--green)'},
  {name:'Agent Coordination',icon:'fa-users-gear',desc:'A2A protocol: Diagnostic Agent, Explanation Agent, Safety Agent, Supervisor Agent (NeuroMCP)',color:'var(--green-light)'},
  {name:'Governance',icon:'fa-gavel',desc:'Content filtering, PII masking, consent verification, audit logging, human escalation triggers',color:'var(--gold-dark)'}
];

// ===== AI TECHNIQUES =====
const aiTechniques = [
  {name:'Machine Learning (ML)',abbr:'ML',icon:'fa-cogs',color:'var(--green)',
   desc:'Classical algorithms: Random Forest, SVM, XGBoost, VotingClassifier. Feature-engineered inputs from EEG spectral/temporal/connectivity domains.',
   flow:['Raw EEG Data','Feature Extraction (200+)','Feature Selection (ANOVA, MI)','Train/Test Split (80/20)','Model Training (RF, SVM, XGB)','Hyperparameter Tuning','Cross-Validation (k=10)','Ensemble (VotingClassifier)','Prediction + Confidence'],
   tools:['scikit-learn','XGBoost','Optuna','SHAP','joblib'],
   metrics:'ASD 97.67%, PD 100%, Epilepsy 99.02%',
   strengths:['Interpretable','Fast inference','Works with small data','Feature importance built-in'],
   limitations:['Manual feature engineering','Limited temporal modeling','Less effective on raw signals']},
  {name:'Deep Learning (DL)',abbr:'DL',icon:'fa-brain',color:'var(--maroon)',
   desc:'Neural networks: CNN, LSTM, CNN-LSTM, Bi-LSTM+Attention. Learns features directly from raw/processed EEG signals.',
   flow:['Raw/Filtered EEG','Epoch Segmentation','Tensor Conversion','CNN Feature Maps','LSTM Temporal Encoding','Attention Mechanism','Dense Classification','Softmax Output','Confidence Score'],
   tools:['PyTorch','TensorFlow','Keras','ONNX Runtime','TensorBoard'],
   metrics:'CNN-LSTM best: ASD 97.67%, PD 100%',
   strengths:['Automatic feature learning','Temporal dynamics capture','Transfer learning','Scalable to raw signals'],
   limitations:['Requires large datasets','Black-box decisions','GPU-dependent','Longer training time']},
  {name:'Computer Vision (CV)',abbr:'CV',icon:'fa-eye',color:'var(--navy)',
   desc:'EEG topographic maps, spectrograms, and time-frequency images processed as visual inputs for CNN-based classification.',
   flow:['EEG Channels','Topographic Map Generation','Spectrogram Creation','Time-Frequency Images','CNN Feature Extraction','Spatial Pattern Recognition','Classification','Grad-CAM Visualization','Clinical Interpretation'],
   tools:['MNE-Python (topomap)','matplotlib (spectrogram)','OpenCV','ResNet/VGG backbone','Grad-CAM'],
   metrics:'Topomap CNN: ASD 95.2%, PD 98.1%',
   strengths:['Spatial pattern capture','Transfer learning from ImageNet','Visual explainability via Grad-CAM','Multi-channel synthesis'],
   limitations:['Information loss in 2D projection','Resolution trade-offs','Compute-heavy for real-time']},
  {name:'Natural Language Processing (NLP)',abbr:'NLP',icon:'fa-language',color:'var(--teal)',
   desc:'Clinical notes processing, RAG-generated explanations, medical literature retrieval, patient report generation.',
   flow:['Clinical Notes / Literature','Tokenization','Embedding (768-dim)','Named Entity Recognition','Medical Concept Extraction','Sentiment / Severity Analysis','Report Template Selection','Natural Language Generation','Patient-Friendly Output'],
   tools:['Sentence Transformers','spaCy (biomedical)','BioBERT','MedSpaCy','Hugging Face'],
   metrics:'NER F1: 0.91, Report quality: 4.6/5 expert rating',
   strengths:['Medical terminology understanding','Multilingual potential','Context-aware generation','Literature grounding'],
   limitations:['Domain-specific training needed','Hallucination risk','Ambiguity in clinical text']},
  {name:'Retrieval-Augmented Generation (RAG)',abbr:'RAG',icon:'fa-magnifying-glass',color:'var(--gold-dark)',
   desc:'ChromaDB vector store (1.4 GB), semantic retrieval of medical knowledge, grounded explanations with citation validation.',
   flow:['User Query + Prediction','Query Expansion','Vector Similarity Search (ChromaDB)','Top-5 Context Retrieval','Re-ranking (relevance)','Prompt Assembly (context + query)','LLM Generation','Hallucination Check','Citation Validation','Faithfulness Score','Final Output'],
   tools:['ChromaDB','Sentence Transformers','RAGAS','LangChain','Custom hallucination detector'],
   metrics:'Faithfulness 0.92, Relevance 0.89, Precision 0.94',
   strengths:['Grounded in real medical literature','Reduced hallucination','Updatable knowledge base','Citation traceability'],
   limitations:['Retrieval quality depends on corpus','Latency from retrieval step','Chunk boundary issues']}
];

// ===== B2C / B2B =====
const b2cB2b = {
  b2c: {title:'B2C: Consumer Health',icon:'fa-user',color:'var(--green)',
    items:[
      {label:'Home EEG Monitoring',desc:'Consumer wearable (Emotiv Insight/EPOC X) for at-home neurological screening'},
      {label:'Mobile Health App',desc:'Real-time results, plain-language explanations, health tracking, trend analysis'},
      {label:'Wellness & Prevention',desc:'Stress monitoring, meditation feedback, sleep quality, cognitive performance'},
      {label:'Early Detection',desc:'Pre-clinical screening for ASD (children), PD (elderly), depression (all ages)'},
      {label:'Telehealth Integration',desc:'Share results with clinicians remotely, reduce in-person visits'},
      {label:'Family Health Dashboard',desc:'Multi-user profiles, pediatric mode for ASD screening, elderly care alerts'}
    ]},
  b2b: {title:'B2B: Enterprise Health',icon:'fa-building',color:'var(--navy)',
    items:[
      {label:'Hospital AI Platform',desc:'Clinical-grade diagnostic AI with governance, audit trails, regulatory compliance'},
      {label:'Insurance Risk Scoring',desc:'AI-driven neurological risk assessment for policy underwriting and claims'},
      {label:'Pharma Clinical Trials',desc:'EEG biomarker endpoints, patient stratification, treatment response monitoring'},
      {label:'Workplace Wellness',desc:'Employee stress/burnout monitoring (opt-in), occupational health compliance'},
      {label:'Research Institutions',desc:'Multi-site EEG analysis platform, federated learning, data governance'},
      {label:'Medical Device Companies',desc:'White-label AI engine for EEG device manufacturers, governance-as-a-service'}
    ]}
};

// ===== AI LEVERS =====
const aiLevers = [
  {name:'Diagnostic Accuracy',icon:'fa-bullseye',value:'90.8% MSCA',desc:'Multi-domain ensemble AI achieves near-clinical accuracy across 5 diseases',color:'var(--green)'},
  {name:'Speed to Diagnosis',icon:'fa-bolt',value:'Minutes vs Months',desc:'From 6-18 month specialist wait to real-time AI-powered screening',color:'var(--maroon)'},
  {name:'Cost Reduction',icon:'fa-piggy-bank',value:'97% Lower',desc:'$300-800 consumer wearable vs $50K-200K clinical EEG',color:'var(--navy)'},
  {name:'Scale & Access',icon:'fa-globe',value:'Global Reach',desc:'Any patient with a wearable device, anywhere, anytime — no specialist needed',color:'var(--teal)'},
  {name:'Explainability',icon:'fa-lightbulb',value:'0.92 Faithfulness',desc:'RAG-powered plain-language explanations patients and clinicians can trust',color:'var(--gold-dark)'},
  {name:'Governance',icon:'fa-shield-halved',value:'525 Modules',desc:'Built-in compliance (EU AI Act, FDA, HIPAA) — not bolted on after',color:'var(--maroon-light)'},
  {name:'Multi-Disease',icon:'fa-viruses',value:'5+ Diseases',desc:'Single framework governs ASD, PD, epilepsy, stress, depression — extensible',color:'var(--green-light)'},
  {name:'Continuous Learning',icon:'fa-arrows-spin',value:'Auto-Retrain',desc:'Drift detection triggers retraining — models improve with more data',color:'var(--navy-light)'}
];

// ===== DRIVERS =====
const drivers = [
  {category:'Technology',icon:'fa-microchip',color:'var(--green)',items:['Consumer EEG wearable maturity (Emotiv, Muse, NeuroSky)','Cloud AI/ML infrastructure (GPU, serverless)','RAG & LLM breakthroughs (GPT-4, Claude, Gemini)','Edge computing for real-time inference','Agentic AI orchestration (MCP, A2A)']},
  {category:'Market',icon:'fa-chart-line',color:'var(--maroon)',items:['$1.5T global mental health market by 2030','970M people with mental health disorders (WHO)','Consumer health tech adoption post-COVID','Telehealth normalization','Direct-to-consumer health device boom']},
  {category:'Regulatory',icon:'fa-gavel',color:'var(--navy)',items:['EU AI Act (2024) — high-risk AI governance mandate','FDA SaMD guidance — predetermined change control','ISO/IEC 42001:2023 — AI management systems','HIPAA/GDPR — health data governance','State-level AI regulations emerging']},
  {category:'Social',icon:'fa-users',color:'var(--teal)',items:['Patient demand for faster diagnosis','Health equity and access gaps (rural/developing)','Mental health destigmatization','Aging population (PD, dementia)','Neurodiversity awareness (ASD)']}
];

// ===== PPPT FRAMEWORK (People, Profit, Process, Technology) =====
const ppptFramework = [
  {pillar:'People',icon:'fa-users',color:'var(--green)',
   items:['AI governance board (5-7 members)','Data scientists (ML/DL/NLP)','Clinical advisory panel','Ethics review committee','Patient advocacy group','Regulatory affairs team'],
   kpis:['Team competency score','Training hours per quarter','Expert panel satisfaction','Patient trust score']},
  {pillar:'Profit',icon:'fa-chart-line',color:'var(--maroon)',
   items:['287% ROI (3-year projection)','$200K-500K annual compliance savings','Reduced misdiagnosis cost ($5K/case)','New revenue: governance-as-a-service','Insurance premium reduction','Faster clinical trial enrollment'],
   kpis:['ROI percentage','Cost per diagnosis','Revenue per patient','Compliance cost reduction']},
  {pillar:'Process',icon:'fa-gears',color:'var(--navy)',
   items:['End-to-end diagnostic pipeline','MLOps + LLMOps automation','4-level risk escalation','525-module quality gates','Continuous monitoring & retraining','Audit trail generation'],
   kpis:['Diagnosis turnaround time','Model drift detection rate','Escalation resolution time','Quality gate pass rate']},
  {pillar:'Technology',icon:'fa-laptop-code',color:'var(--teal)',
   items:['Consumer wearable EEG (4-32 ch)','Cloud ML/DL platform','RAG engine (ChromaDB 1.4 GB)','Agentic orchestration (MCP/A2A)','Mobile app (React Native)','Governance decision engine'],
   kpis:['Inference latency (<100ms)','System uptime (99.9%)','Model accuracy (>90%)','RAG faithfulness (>0.90)']}
];

// ===== OPEN SOURCE MODELS =====
const openSourceModels = [
  {name:'Llama 3.1',org:'Meta',params:'8B / 70B / 405B',license:'Llama 3.1 Community',useCase:'RAG explanations, clinical report generation',color:'var(--navy)'},
  {name:'Mistral',org:'Mistral AI',params:'7B / 8x7B (Mixtral)',license:'Apache 2.0',useCase:'Lightweight inference, edge deployment, fast explanations',color:'var(--green)'},
  {name:'Gemma 2',org:'Google',params:'2B / 9B / 27B',license:'Gemma License',useCase:'On-device inference, mobile deployment, small language model',color:'var(--teal)'},
  {name:'BioMistral',org:'Community',params:'7B',license:'Apache 2.0',useCase:'Biomedical-specific RAG, clinical NER, medical QA',color:'var(--maroon)'},
  {name:'Phi-3',org:'Microsoft',params:'3.8B / 14B',license:'MIT',useCase:'Edge AI, low-latency inference, resource-constrained devices',color:'var(--gold-dark)'},
  {name:'Qwen 2.5',org:'Alibaba',params:'7B / 72B',license:'Apache 2.0',useCase:'Multilingual explanations, cross-cultural medical reports',color:'var(--maroon-light)'}
];

// ===== DATABASE TYPES =====
const databaseTypes = [
  {name:'Graph Database',type:'graph',icon:'fa-diagram-project',color:'var(--green)',
   tech:'Neo4j / Amazon Neptune',
   useCase:'Disease-symptom-gene knowledge graph, drug interaction networks, patient relationship mapping',
   schema:'Nodes: Disease, Symptom, Gene, Drug, Patient | Edges: causes, treats, interacts_with, diagnosed_with',
   queries:['MATCH (d:Disease)-[:HAS_BIOMARKER]->(b:Biomarker) WHERE d.name="ASD" RETURN b','MATCH path = shortestPath((p:Patient)-[*]-(d:Disease)) RETURN path','MATCH (d1:Drug)-[:INTERACTS_WITH]->(d2:Drug) RETURN d1, d2'],
   benefits:['Multi-hop reasoning for differential diagnosis','Drug interaction safety checks','Pathway analysis for treatment planning','Explainable relationships for RAG grounding']},
  {name:'Vector Database',type:'vector',icon:'fa-vector-square',color:'var(--navy)',
   tech:'ChromaDB / Pinecone / Weaviate',
   useCase:'Semantic search over medical literature, EEG pattern matching, RAG retrieval engine',
   schema:'Collections: medical_literature (1.4 GB), eeg_patterns, clinical_guidelines | Embedding: 768-dim sentence transformers',
   queries:['collection.query(query_texts=["ASD frontal gamma patterns"], n_results=5)','similarity_search(embedding, threshold=0.85)','hybrid_search(sparse_bm25 + dense_vector, alpha=0.7)'],
   benefits:['Semantic similarity beyond keyword matching','Sub-second retrieval from 1.4 GB corpus','Supports hybrid search (sparse + dense)','Foundation for RAG pipeline']},
  {name:'Time-Series Database',type:'timeseries',icon:'fa-clock',color:'var(--maroon)',
   tech:'InfluxDB / TimescaleDB / Apache IoTDB',
   useCase:'EEG signal storage, real-time monitoring, device telemetry, drift detection history',
   schema:'Measurements: eeg_signal (timestamp, channel, value), device_health (battery, impedance), model_metrics (accuracy, drift_score)',
   queries:['SELECT mean(value) FROM eeg_signal WHERE channel=\'AF3\' AND time > now()-1h GROUP BY time(2s)','SELECT derivative(accuracy) FROM model_metrics WHERE disease=\'ASD\'','SELECT * FROM drift_scores WHERE psi > 0.2'],
   benefits:['Optimized for high-frequency EEG data (256 Hz × 32 channels)','Built-in downsampling and retention policies','Real-time aggregation for monitoring dashboards','Efficient storage compression for signal data']}
];

// ===== MCP PIPELINE ARCHITECTURE =====
const mcpPipeline = [
  {stage:'Emotiv Device',icon:'fa-head-side-virus',color:'var(--green-dark)',
   details:'EPOC X (14 ch) / Insight (5 ch) / EPOC Flex (32 ch)',
   specs:['128/256 Hz sampling','14-bit ADC resolution','BLE 5.0 / USB dongle','Ag/AgCl + saline electrodes','Battery: 6-12 hours','Impedance monitoring']},
  {stage:'IoT Gateway',icon:'fa-network-wired',color:'var(--green)',
   details:'Edge preprocessing + secure transmission',
   specs:['Raspberry Pi / Mobile phone','Signal quality check (SNR ≥ 10 dB)','Buffer management (2-4s epochs)','BLE → WiFi bridge','TLS 1.3 encryption','Local artifact rejection']},
  {stage:'MCP Server',icon:'fa-server',color:'var(--teal)',
   details:'Model Context Protocol — tool orchestration',
   specs:['RESTful API endpoints','Tool registry (10+ tools)','Context management','Session state tracking','Authentication (API key)','Rate limiting (100 req/min)']},
  {stage:'Data Layer',icon:'fa-database',color:'var(--navy-light)',
   details:'Multi-database architecture',
   specs:['TimescaleDB (EEG signals)','ChromaDB (1.4 GB vectors)','Neo4j (knowledge graph)','PostgreSQL (metadata)','Redis (session cache)','S3 (raw data archive)']},
  {stage:'Filter + Preprocess',icon:'fa-filter',color:'var(--navy)',
   details:'Signal conditioning pipeline',
   specs:['Bandpass 0.5-100 Hz (Butterworth)','Notch filter 50/60 Hz','ICA artifact removal','Epoch segmentation (2-4s)','Z-score normalization','Bad channel interpolation']},
  {stage:'Model Inference',icon:'fa-brain',color:'var(--maroon)',
   details:'ML/DL ensemble prediction',
   specs:['198 trained models (joblib)','CNN-LSTM architecture','VotingClassifier ensemble','Confidence scoring','SHAP explanation','< 100ms latency']},
  {stage:'RAG Engine',icon:'fa-magnifying-glass',color:'var(--maroon-light)',
   details:'Retrieval-augmented generation',
   specs:['Query expansion','ChromaDB similarity search','Top-5 context retrieval','Re-ranking (cross-encoder)','Prompt assembly','Citation validation']},
  {stage:'Output Evaluation',icon:'fa-check-double',color:'var(--gold-dark)',
   details:'Quality assurance + governance',
   specs:['Faithfulness check (≥ 0.90)','Hallucination detection','Risk scoring (4-level)','Audit trail logging','Clinician escalation trigger','Patient report generation']}
];

// ===== PATIENT JOURNEY =====
const patientJourney = [
  {phase:'Awareness',icon:'fa-lightbulb',color:'var(--green-dark)',duration:'Ongoing',
   touchpoints:['Symptom recognition','Family/friend concern','Online health research','Healthcare provider suggestion'],
   painPoints:['Uncertainty about symptoms','Information overload','Stigma (mental health)','Fear of diagnosis'],
   rgaigValue:'Educational content via app, symptom self-assessment tool'},
  {phase:'Device Setup',icon:'fa-plug',color:'var(--green)',duration:'15-30 min',
   touchpoints:['Purchase wearable (online/clinic)','App download','Account creation','Device pairing'],
   painPoints:['Technical setup complexity','Privacy concerns','Cost barrier ($300-800)','Electrode placement learning'],
   rgaigValue:'Guided setup wizard, video tutorials, privacy-first design'},
  {phase:'EEG Recording',icon:'fa-wave-square',color:'var(--teal)',duration:'5-20 min',
   touchpoints:['Electrode placement','Signal quality check','Recording session','Real-time feedback'],
   painPoints:['Signal artifacts','Electrode discomfort','Session duration','Environmental noise'],
   rgaigValue:'Automated quality monitoring, guided positioning, adaptive session length'},
  {phase:'AI Analysis',icon:'fa-robot',color:'var(--navy)',duration:'< 2 min',
   touchpoints:['Signal processing','Feature extraction','Model inference','RAG explanation'],
   painPoints:['Waiting anxiety','Black box concern','Trust in AI','Understanding results'],
   rgaigValue:'Real-time progress indicator, transparent processing steps, confidence display'},
  {phase:'Results & Explanation',icon:'fa-file-medical',color:'var(--maroon)',duration:'Immediate',
   touchpoints:['Diagnostic result','Confidence score','Plain-language explanation','Clinical detail (optional)'],
   painPoints:['Result anxiety','Medical jargon','Misinterpretation','Next steps unclear'],
   rgaigValue:'Dual-track reports (consumer + clinical), actionable recommendations, FAQ'},
  {phase:'Clinical Follow-up',icon:'fa-user-doctor',color:'var(--maroon-dark)',duration:'1-7 days',
   touchpoints:['Share with clinician','Telehealth consultation','Referral if needed','Treatment plan'],
   painPoints:['Specialist access','Cost of consultation','Coordinating records','Treatment uncertainty'],
   rgaigValue:'Direct clinician sharing, telehealth integration, clinical-grade report'},
  {phase:'Ongoing Monitoring',icon:'fa-chart-line',color:'var(--gold-dark)',duration:'Continuous',
   touchpoints:['Regular screenings','Trend tracking','Medication response','Lifestyle adjustments'],
   painPoints:['Compliance fatigue','Data overload','Progress uncertainty','Motivation'],
   rgaigValue:'Personalized dashboards, trend alerts, milestone celebrations, care team sync'}
];

// ===== IMPACT METRICS =====
const impactMetrics = [
  {category:'Clinical Impact',icon:'fa-heart-pulse',color:'var(--maroon)',metrics:[
    {label:'Diagnostic Accuracy',value:'90.8%',baseline:'70-85%',improvement:'+15-20%'},
    {label:'Misdiagnosis Reduction',value:'85%',baseline:'15-30% error rate',improvement:'-85% errors'},
    {label:'Time to Diagnosis',value:'< 5 min',baseline:'6-18 months',improvement:'99.9% faster'},
    {label:'Disease Coverage',value:'5 domains',baseline:'1 per tool',improvement:'5x coverage'},
    {label:'Explainability',value:'0.92 faithfulness',baseline:'Black box',improvement:'Full transparency'}
  ]},
  {category:'Economic Impact',icon:'fa-coins',color:'var(--green)',metrics:[
    {label:'Cost per Diagnosis',value:'$5-20',baseline:'$2,000-5,000',improvement:'99% reduction'},
    {label:'Equipment Cost',value:'$300-800',baseline:'$50K-200K',improvement:'97% reduction'},
    {label:'ROI (3-Year)',value:'287%',baseline:'N/A',improvement:'Positive Year 2'},
    {label:'Compliance Savings',value:'$200K-500K/yr',baseline:'$500K-1M/yr',improvement:'50-60% savings'},
    {label:'Revenue Potential',value:'$50M+ TAM',baseline:'N/A',improvement:'New market'}
  ]},
  {category:'Social Impact',icon:'fa-globe',color:'var(--navy)',metrics:[
    {label:'Access Expansion',value:'Global',baseline:'Urban/specialist only',improvement:'Rural + developing'},
    {label:'Wait Time Reduction',value:'99.9%',baseline:'6-18 months',improvement:'Instant screening'},
    {label:'Health Equity',value:'Any wearable user',baseline:'Specialist access only',improvement:'Democratized'},
    {label:'Patient Empowerment',value:'Self-monitoring',baseline:'Clinician-dependent',improvement:'Autonomous'},
    {label:'Mental Health Stigma',value:'Private screening',baseline:'Clinical visit',improvement:'Reduced barrier'}
  ]}
];

// ===== VALUE REALIZATION MATRIX =====
const valueMatrix = [
  {stakeholder:'Patients',shortTerm:'Faster screening (minutes), lower cost ($300-800 device)',mediumTerm:'Continuous monitoring, trend tracking, medication response',longTerm:'Personalized prevention, early intervention, improved outcomes',metrics:'Wait time, cost, satisfaction, health outcomes'},
  {stakeholder:'Clinicians',shortTerm:'AI-assisted diagnosis, reduced workload, SHAP explanations',mediumTerm:'Multi-disease platform, evidence-based decisions, RAG reports',longTerm:'Precision medicine, population health insights, research data',metrics:'Diagnostic accuracy, time saved, patient throughput'},
  {stakeholder:'Hospitals',shortTerm:'Reduced misdiagnosis liability, compliance automation',mediumTerm:'AI governance platform, audit trail, regulatory readiness',longTerm:'AI center of excellence, industry leadership, new revenue',metrics:'ROI, compliance cost, patient volume, risk reduction'},
  {stakeholder:'Insurers',shortTerm:'Better risk assessment, fraud detection',mediumTerm:'Predictive models for claims, early intervention incentives',longTerm:'Population health management, precision underwriting',metrics:'Claims accuracy, loss ratio, customer retention'},
  {stakeholder:'Regulators',shortTerm:'Transparent AI decisions, audit trail availability',mediumTerm:'Standardized governance framework, cross-jurisdictional alignment',longTerm:'Evidence-based regulation, industry benchmark',metrics:'Compliance rate, incident reports, governance maturity'},
  {stakeholder:'Researchers',shortTerm:'Multi-site EEG data access, standardized pipelines',mediumTerm:'Federated learning, biomarker discovery, longitudinal data',longTerm:'New disease models, treatment response prediction, global collaboration',metrics:'Publications, dataset access, model contributions'}
];

// ===== ROI MATRIX =====
const roiMatrix = [
  {item:'Wearable Devices (100 units)',cost:'$80,000',year1:'$0',year2:'$120,000',year3:'$180,000',roi:'275%',category:'Hardware'},
  {item:'Cloud Infrastructure',cost:'$60,000/yr',year1:'$60,000',year2:'$60,000',year3:'$60,000',roi:'Operational',category:'Infrastructure'},
  {item:'AI Model Development',cost:'$150,000',year1:'$50,000',year2:'$100,000',year3:'$200,000',roi:'133%',category:'Development'},
  {item:'Governance Platform',cost:'$80,000',year1:'$100,000',year2:'$250,000',year3:'$400,000',roi:'400%',category:'Software'},
  {item:'Regulatory Compliance',cost:'$50,000',year1:'$200,000',year2:'$350,000',year3:'$500,000',roi:'900%',category:'Compliance'},
  {item:'Staff Training',cost:'$30,000',year1:'$20,000',year2:'$40,000',year3:'$60,000',roi:'100%',category:'People'},
  {item:'Patient Acquisition',cost:'$40,000/yr',year1:'$100,000',year2:'$300,000',year3:'$500,000',roi:'525%',category:'Marketing'},
  {item:'TOTAL',cost:'$490,000',year1:'$530,000',year2:'$1,220,000',year3:'$1,900,000',roi:'287%',category:'Summary'}
];

// ===== KPI MATRIX =====
const kpiMatrix = [
  {domain:'Clinical',kpis:[
    {name:'MSCA (Multi-Site Cross-validated Accuracy)',target:'≥ 90%',actual:'90.8%',status:'pass',frequency:'Monthly'},
    {name:'Mean AUC-ROC',target:'≥ 0.95',actual:'0.956',status:'pass',frequency:'Monthly'},
    {name:'Macro F1 Score',target:'≥ 0.90',actual:'0.912',status:'pass',frequency:'Monthly'},
    {name:'Misdiagnosis Rate',target:'≤ 5%',actual:'3.2%',status:'pass',frequency:'Weekly'},
    {name:'Time to Diagnosis',target:'< 5 min',actual:'2.3 min',status:'pass',frequency:'Real-time'}
  ]},
  {domain:'Governance',kpis:[
    {name:'525-Module Pass Rate',target:'≥ 95%',actual:'97.9%',status:'pass',frequency:'Quarterly'},
    {name:'Audit Trail Completeness',target:'100%',actual:'100%',status:'pass',frequency:'Daily'},
    {name:'Risk Escalation Response',target:'< 15 min',actual:'8 min',status:'pass',frequency:'Real-time'},
    {name:'Regulatory Alignment Score',target:'≥ 90%',actual:'94%',status:'pass',frequency:'Quarterly'},
    {name:'Bias Detection Rate',target:'100% flagged',actual:'100%',status:'pass',frequency:'Weekly'}
  ]},
  {domain:'Operational',kpis:[
    {name:'System Uptime',target:'≥ 99.9%',actual:'99.95%',status:'pass',frequency:'Real-time'},
    {name:'Inference Latency',target:'< 100ms',actual:'67ms',status:'pass',frequency:'Real-time'},
    {name:'Model Drift (PSI)',target:'< 0.2',actual:'0.08',status:'pass',frequency:'Weekly'},
    {name:'RAG Faithfulness',target:'≥ 0.90',actual:'0.92',status:'pass',frequency:'Daily'},
    {name:'Data Pipeline Throughput',target:'≥ 1000 records/min',actual:'1,450/min',status:'pass',frequency:'Real-time'}
  ]},
  {domain:'Business',kpis:[
    {name:'ROI',target:'≥ 200%',actual:'287%',status:'pass',frequency:'Annually'},
    {name:'Patient Satisfaction',target:'≥ 4.0/5',actual:'4.6/5',status:'pass',frequency:'Monthly'},
    {name:'Cost per Diagnosis',target:'≤ $20',actual:'$12',status:'pass',frequency:'Monthly'},
    {name:'Expert Panel Rating',target:'≥ 4.0/5',actual:'4.6/5',status:'pass',frequency:'Quarterly'},
    {name:'Compliance Cost Reduction',target:'≥ 40%',actual:'55%',status:'pass',frequency:'Annually'}
  ]}
];

// ===== FEATURE MATRIX =====
const featureMatrix = [
  {feature:'Multi-Domain Diagnosis',rgaig:'5 diseases, extensible',competitor1:'Single disease',competitor2:'1-2 diseases',competitor3:'3 diseases'},
  {feature:'Governance Framework',rgaig:'525 modules, 9 layers',competitor1:'Basic policies',competitor2:'ISO-aligned',competitor3:'Ad hoc'},
  {feature:'Consumer Wearable Support',rgaig:'4-32 ch (Emotiv+)',competitor1:'Clinical only',competitor2:'Research only',competitor3:'14 ch only'},
  {feature:'RAG Explanations',rgaig:'0.92 faithfulness',competitor1:'None',competitor2:'Template-based',competitor3:'Basic NLG'},
  {feature:'Agentic Orchestration',rgaig:'4-agent MCP/A2A',competitor1:'None',competitor2:'None',competitor3:'Single agent'},
  {feature:'Drift Detection',rgaig:'PSI/CSI, auto-retrain',competitor1:'Manual review',competitor2:'None',competitor3:'Basic alerts'},
  {feature:'Regulatory Compliance',rgaig:'EU AI Act, FDA, ISO, NIST',competitor1:'EU AI Act only',competitor2:'ISO only',competitor3:'None'},
  {feature:'Trust Model',rgaig:'TAM-TOE-RBV (validated)',competitor1:'None',competitor2:'Survey only',competitor3:'None'},
  {feature:'Statistical Validation',rgaig:'k-fold, LOSO, bootstrap CI',competitor1:'Train/test only',competitor2:'k-fold only',competitor3:'Holdout only'},
  {feature:'Expert Panel',rgaig:'12 experts, 4.6/5',competitor1:'None',competitor2:'3 reviewers',competitor3:'None'},
  {feature:'Open Source Option',rgaig:'Llama/Mistral/Phi-3',competitor1:'Proprietary only',competitor2:'GPT-4 only',competitor3:'Proprietary only'},
  {feature:'Edge Deployment',rgaig:'ONNX, TFLite, < 500MB',competitor1:'Cloud only',competitor2:'Cloud only',competitor3:'Partial'},
  {feature:'Carbon Tracking',rgaig:'CodeCarbon integrated',competitor1:'None',competitor2:'None',competitor3:'None'},
  {feature:'Knowledge Graph',rgaig:'Neo4j disease-symptom',competitor1:'None',competitor2:'None',competitor3:'Basic ontology'},
  {feature:'Patient Journey',rgaig:'7-phase, app-guided',competitor1:'Clinician-only',competitor2:'Web portal',competitor3:'None'}
];

// ===== CASE STUDIES =====
const caseStudies = [
  {title:'Pediatric ASD Screening Program',domain:'Autism',icon:'fa-child',color:'var(--navy)',
   challenge:'6-18 month wait for ASD specialist evaluation. 1 in 36 children affected. Early intervention critical before age 3.',
   solution:'Home-based EEG screening using Emotiv EPOC X (14 channels). RGAIG+ CNN-LSTM model processes 5-minute recording. RAG generates parent-friendly explanation.',
   results:['97.67% accuracy (300 subjects)','5-minute screening vs 18-month wait','$300 device vs $5,000 clinical assessment','Parent satisfaction: 4.7/5'],
   impact:'Potential to screen 100,000+ children annually, enabling early intervention during critical neurodevelopmental window.'},
  {title:'Elderly PD Early Detection',domain:'Parkinson\'s',icon:'fa-person-cane',color:'var(--maroon)',
   challenge:'PD diagnosed after 60-80% dopaminergic neuron loss. Current diagnosis relies on motor symptoms — too late for neuroprotection.',
   solution:'Longitudinal EEG monitoring with consumer wearable. RGAIG+ detects pre-motor EEG biomarkers (excessive beta, slowed background). Automated clinician alerts.',
   results:['100% accuracy on validation set (50 subjects)','Detects pre-clinical changes 2-5 years earlier','Continuous monitoring during daily activities','Clinician alert in < 2 minutes'],
   impact:'Early PD detection enables neuroprotective interventions, potentially delaying motor symptom onset by 3-5 years.'},
  {title:'Workplace Stress Monitoring',domain:'Stress',icon:'fa-building',color:'var(--green)',
   challenge:'77% of employees experience work stress. $300B annual cost to US employers. Burnout leads to turnover, absenteeism, reduced productivity.',
   solution:'Opt-in workplace wellness program using Emotiv Insight (5 channels). 5-minute daily check-in. RGAIG+ stress detection with privacy-preserved aggregate reporting.',
   results:['94.17% accuracy (120 subjects)','23% reduction in reported burnout','15% improvement in productivity metrics','Employee satisfaction: 4.3/5'],
   impact:'Scalable to Fortune 500 companies. Privacy-first design (individual data never shared with employer). Aggregate insights drive organizational interventions.'},
  {title:'Hospital Epilepsy Monitoring',domain:'Epilepsy',icon:'fa-hospital',color:'var(--teal)',
   challenge:'Epilepsy affects 50M globally. Hospital EEG monitoring requires 24-72 hour stay. Consumer wearables could extend monitoring to home.',
   solution:'Extended home monitoring with 32-channel clinical-grade EEG. RGAIG+ real-time seizure detection with automated clinician escalation. Governance-compliant audit trail.',
   results:['99.02% accuracy (102 subjects, Bonn dataset)','Real-time detection < 2 seconds','Reduced hospital stays by 60%','FDA SaMD pathway initiated'],
   impact:'Home-based epilepsy monitoring reduces hospital burden by 60%, improves patient quality of life, and enables 24/7 automated surveillance.'}
];

// ===== COMPREHENSIVE RGAIG+ SURVEY (8 Categories × 5 Questions = 40 Total) =====
const surveyCategories = [
  {id:'technology',name:'Technology & Platform',icon:'fa-microchip',color:'#2563eb',
   desc:'Evaluate the RGAIG+ hardware (EEG wearables), software stack (ML/DL, RAG, agentic AI), and platform readiness.',
   questions:[
     {id:'TP1',text:'The 9-layer architecture (device → signal → model → GenAI → agent → interface → clinical → monitoring → governance) provides comprehensive end-to-end coverage.',weight:1.2,dimension:'Architecture'},
     {id:'TP2',text:'Consumer EEG wearables (Emotiv EPOC X, 14 channels, SNR >= 10 dB) provide adequate signal quality for multi-disease screening.',weight:1.1,dimension:'Hardware'},
     {id:'TP3',text:'The ML/DL pipeline (CNN-LSTM, VotingClassifier, ensemble) with agentic orchestration (MCP/A2A) is technically sound and production-ready.',weight:1.2,dimension:'Software'},
     {id:'TP4',text:'The RAG engine (ChromaDB 1.4 GB, 0.92 faithfulness) produces grounded, citation-backed clinical explanations — not hallucinated outputs.',weight:1.1,dimension:'RAG Engine'},
     {id:'TP5',text:'The 525-module quality taxonomy across 3 tiers (ML/DL, GenAI QA, AI Governance Pillars) is thorough and well-structured.',weight:1.0,dimension:'Taxonomy'}
   ]},
  {id:'data_model',name:'Data & Model Accuracy',icon:'fa-brain',color:'#059669',
   desc:'Evaluate data quality, model performance, disease-specific validation, and statistical rigor.',
   questions:[
     {id:'DM1',text:'The dataset (305 GB, 768+ subjects across 5 diseases) with demographic diversity is sufficient for reliable multi-domain validation.',weight:1.2,dimension:'Data Quality'},
     {id:'DM2',text:'MSCA of 90.8% with per-disease accuracy (ASD 97.67%, PD 100%, Epilepsy 99.02%, Stress 94.17%, Depression 91.07%) meets clinical screening thresholds.',weight:1.2,dimension:'Accuracy'},
     {id:'DM3',text:'Statistical rigor (k-fold CV, LOSO, bootstrap CI with 1,000 resamples, ablation study) provides sufficient evidence of model robustness.',weight:1.1,dimension:'Validation'},
     {id:'DM4',text:'Data quality monitoring (PSI/CSI drift detection, automated retraining triggers) prevents model degradation over time.',weight:1.0,dimension:'Monitoring'},
     {id:'DM5',text:'Cross-disease transfer learning and comorbidity handling demonstrate the framework\'s multi-domain generalization capability.',weight:1.0,dimension:'Generalization'}
   ]},
  {id:'trust_explain',name:'Explainability & Trust',icon:'fa-lightbulb',color:'#7c3aed',
   desc:'Evaluate how transparently RGAIG+ communicates reasoning, builds clinician trust, and ensures patient understanding.',
   questions:[
     {id:'TE1',text:'SHAP-based feature attribution identifies which specific EEG channels and frequency bands drove each prediction — enabling clinical interpretation.',weight:1.2,dimension:'Explainability'},
     {id:'TE2',text:'Dual-track reporting (plain-language consumer summary + detailed clinical narrative with SHAP plots and citations) serves both audiences effectively.',weight:1.1,dimension:'Reporting'},
     {id:'TE3',text:'Clinicians retain final diagnostic authority — RGAIG+ positions itself as decision-support, not autonomous decision-maker.',weight:1.2,dimension:'Trust'},
     {id:'TE4',text:'The system flags uncertain predictions (low confidence, borderline scores, ensemble disagreement) rather than presenting all outputs with equal certainty.',weight:1.1,dimension:'Uncertainty'},
     {id:'TE5',text:'A clinician feedback loop allows diagnostic disputes and corrections that feed back into model improvement.',weight:1.0,dimension:'Feedback'}
   ]},
  {id:'guardrail_safety',name:'Guardrails & Safety',icon:'fa-shield-halved',color:'#dc2626',
   desc:'Evaluate safety mechanisms, hallucination prevention, adversarial robustness, and human-in-the-loop controls.',
   questions:[
     {id:'GS1',text:'Hallucination detection gates reject RAG explanations with faithfulness scores below 0.90 before they reach the patient.',weight:1.2,dimension:'Hallucination'},
     {id:'GS2',text:'A clinical safety stop — automatic escalation to human clinician — triggers for high-risk diagnoses (epilepsy alert, unexpected findings in young patients).',weight:1.2,dimension:'Safety Stop'},
     {id:'GS3',text:'Out-of-distribution detection flags EEG signals from unseen device types, extreme artifacts, or underrepresented demographics.',weight:1.1,dimension:'OOD Detection'},
     {id:'GS4',text:'Adversarial robustness testing (noise injection, signal perturbation) has verified that small changes do not flip diagnostic outcomes.',weight:1.0,dimension:'Adversarial'},
     {id:'GS5',text:'Graceful degradation — when any component fails (device disconnection, model timeout, RAG retrieval failure), the system safely halts rather than producing unreliable outputs.',weight:1.0,dimension:'Graceful Degrad.'}
   ]},
  {id:'people_process',name:'People & Process',icon:'fa-users-gear',color:'#0891b2',
   desc:'Evaluate organizational readiness, workforce capability, pipeline maturity, and governance board structure.',
   questions:[
     {id:'PP1',text:'Your organization has a dedicated AI governance board with cross-functional representation (clinical, engineering, legal, compliance).',weight:1.2,dimension:'Governance Board'},
     {id:'PP2',text:'Clinical staff possess sufficient AI literacy to interpret diagnostic outputs, confidence scores, and SHAP explanations.',weight:1.1,dimension:'AI Literacy'},
     {id:'PP3',text:'The end-to-end diagnostic pipeline (EEG capture → preprocessing → inference → RAG explanation → report) is automated and reproducible.',weight:1.1,dimension:'Automation'},
     {id:'PP4',text:'Quality gates (accuracy threshold, drift check, bias scan) block deployment of underperforming models — no manual overrides allowed.',weight:1.0,dimension:'Quality Gates'},
     {id:'PP5',text:'Leadership commitment to AI governance is reflected in dedicated budgets, KPI tracking, and strategic planning.',weight:1.0,dimension:'Leadership'}
   ]},
  {id:'pain_impact',name:'Customer Pain & Impact',icon:'fa-heart-pulse',color:'#ea580c',
   desc:'Evaluate how effectively RGAIG+ addresses patient pain points, clinician workload, and health equity.',
   questions:[
     {id:'CI1',text:'RGAIG+ effectively reduces diagnostic wait time from 6-18 months (specialist referral) to minutes (wearable + AI screening).',weight:1.2,dimension:'Wait Time'},
     {id:'CI2',text:'Cost reduction from $50K-200K clinical EEG to $300-800 consumer wearable makes neurological screening accessible to underserved populations.',weight:1.1,dimension:'Cost Access'},
     {id:'CI3',text:'The framework addresses health equity gaps — enabling screening in rural areas, developing countries, and communities without specialist access.',weight:1.1,dimension:'Health Equity'},
     {id:'CI4',text:'Clinician workload is meaningfully reduced by AI-assisted triage, automated report generation, and governance documentation.',weight:1.0,dimension:'Workload'},
     {id:'CI5',text:'Patient-facing reports include appropriate medical disclaimers, next-step guidance, clinician referral pathways, and right-to-explanation information.',weight:1.0,dimension:'Patient Safety'}
   ]},
  {id:'governance_decision',name:'Governance & Decision Matrix',icon:'fa-scale-balanced',color:'#4338ca',
   desc:'Evaluate decision-making frameworks, escalation pathways, responsible AI ethics, and accountability structures.',
   questions:[
     {id:'GD1',text:'A formal decision matrix scores each AI deployment against clinical impact, technical readiness, regulatory risk, and bias assessment.',weight:1.2,dimension:'Decision Matrix'},
     {id:'GD2',text:'Diagnostic confidence thresholds are clearly tiered — above 90% auto-reports, 70-90% flags for review, below 70% escalates to clinician.',weight:1.1,dimension:'Threshold Logic'},
     {id:'GD3',text:'Bias testing across protected demographics (age, gender, ethnicity) is conducted before every model deployment, with fairness metrics tracked per subgroup.',weight:1.1,dimension:'Responsible AI'},
     {id:'GD4',text:'Accountability chains clearly define responsibility when an AI diagnosis is wrong — the developer, the deploying institution, or the supervising clinician.',weight:1.0,dimension:'Accountability'},
     {id:'GD5',text:'Post-deployment monitoring triggers (accuracy drift, fairness violation, adverse event) invoke automatic governance review cycles.',weight:1.0,dimension:'Post-Deploy'}
   ]},
  {id:'compliance_pii',name:'Standards, PII & Compliance',icon:'fa-certificate',color:'#0d9488',
   desc:'Evaluate regulatory alignment (ISO 42001, NIST, EU AI Act, FDA), data protection, and PII security.',
   questions:[
     {id:'SC1',text:'ISO/IEC 42001 and NIST AI RMF requirements are operationalized with measurable KPIs — not just referenced in documentation.',weight:1.2,dimension:'Standards'},
     {id:'SC2',text:'EU AI Act high-risk classification requirements and FDA SaMD guidance are incorporated into the model release lifecycle.',weight:1.1,dimension:'Regulatory'},
     {id:'SC3',text:'Patient PII is de-identified before ML training, encrypted at rest (AES-256) and in transit (TLS 1.3), with role-based access control enforced.',weight:1.2,dimension:'PII Security'},
     {id:'SC4',text:'HIPAA and GDPR requirements (minimum necessary standard, DPIA, cross-border transfer mechanisms, breach notification) are operationally enforced.',weight:1.0,dimension:'Data Protection'},
     {id:'SC5',text:'Automated compliance checking continuously validates model behavior against governance policies — not relying solely on periodic manual audits.',weight:1.0,dimension:'Auto Compliance'}
   ]}
];

// ===== COMPREHENSIVE ANALYSIS LIST =====
const analysisList = {
  statistical:[
    {name:'Paired t-test',purpose:'Compare model pairs (ML vs DL)',result:'p < .001',category:'Parametric'},
    {name:'Bonferroni Correction',purpose:'Multiple comparisons adjustment',result:'α = .05/10 = .005',category:'Correction'},
    {name:'Bootstrap CI',purpose:'Non-parametric confidence intervals',result:'1,000 resamples, 95% CI',category:'Non-parametric'},
    {name:'McNemar\'s Test',purpose:'Paired classification comparison',result:'p < .01 (ensemble vs single)',category:'Non-parametric'},
    {name:'Friedman Test',purpose:'Compare multiple classifiers',result:'χ² = 42.3, p < .001',category:'Non-parametric'},
    {name:'Wilcoxon Signed-Rank',purpose:'Non-parametric paired comparison',result:'p < .005 (DL vs ML)',category:'Non-parametric'},
    {name:'DeLong Test',purpose:'Compare AUC-ROC curves',result:'p < .01 (ensemble AUC > single)',category:'Parametric'},
    {name:'Cohen\'s d',purpose:'Effect size measurement',result:'d = 1.42 (large effect)',category:'Effect Size'},
    {name:'Cohen\'s κ',purpose:'Inter-rater agreement',result:'κ = 0.84 (substantial)',category:'Agreement'},
    {name:'Krippendorff\'s α',purpose:'Inter-rater reliability',result:'α = 0.84 (good)',category:'Agreement'},
    {name:'Cronbach\'s α',purpose:'Internal consistency of survey',result:'α = 0.89 (excellent)',category:'Reliability'},
    {name:'ANOVA (One-way)',purpose:'Compare means across groups',result:'F(4,763) = 28.7, p < .001',category:'Parametric'},
    {name:'Chi-Square Test',purpose:'Independence of categorical variables',result:'χ²(4) = 15.6, p < .01',category:'Non-parametric'},
    {name:'Mann-Whitney U',purpose:'Non-parametric group comparison',result:'U = 1245, p < .005',category:'Non-parametric'},
    {name:'Shapiro-Wilk',purpose:'Test normality assumption',result:'W = 0.96, p > .05 (normal)',category:'Assumption'},
    {name:'Levene\'s Test',purpose:'Test homogeneity of variance',result:'F = 1.23, p > .05 (equal)',category:'Assumption'},
    {name:'Kolmogorov-Smirnov',purpose:'Distribution comparison',result:'D = 0.08, p > .05',category:'Distribution'},
    {name:'Spearman\'s ρ',purpose:'Rank correlation',result:'ρ = 0.78, p < .001',category:'Correlation'},
    {name:'Pearson\'s r',purpose:'Linear correlation',result:'r = 0.82, p < .001',category:'Correlation'},
    {name:'Structural Equation Modeling',purpose:'TAM-TOE-RBV path analysis',result:'CFI=0.95, RMSEA=0.04',category:'Multivariate'}
  ],
  sensitivity:[
    {name:'3-Scenario Analysis',method:'Base / Optimistic / Pessimistic',finding:'ROI: 200-375% range',category:'Scenario'},
    {name:'Tornado Diagram',method:'One-at-a-time parameter variation',finding:'Accuracy most sensitive parameter',category:'Parameter'},
    {name:'Leave-One-Subject-Out (LOSO)',method:'Exclude each subject iteratively',finding:'Stable across subjects (CV ± 2.6%)',category:'Validation'},
    {name:'Ablation Study',method:'Remove pipeline components',finding:'Ensemble: +8.3% over single model',category:'Component'},
    {name:'Feature Sensitivity (SHAP)',method:'Permutation importance ranking',finding:'Top-10 features = 82% signal',category:'Feature'},
    {name:'Channel Reduction',method:'32 → 14 → 8 → 4 channels',finding:'14ch retains 94% accuracy',category:'Hardware'},
    {name:'Sample Size Analysis',method:'Learning curves (10% → 100%)',finding:'Plateau at ~200 subjects',category:'Data'},
    {name:'Cross-Domain Transfer',method:'Train on disease A, test on B',finding:'85% accuracy on unseen disease',category:'Transfer'},
    {name:'Adversarial Robustness',method:'FGSM, PGD noise injection',finding:'< 3% accuracy drop at ε=0.05',category:'Robustness'},
    {name:'Temporal Stability',method:'6-month retest reliability',finding:'ICC = 0.89 (excellent)',category:'Stability'},
    {name:'Hyperparameter Sensitivity',method:'Bayesian optimization landscape',finding:'Flat optimum (robust to tuning)',category:'Parameter'},
    {name:'Missing Channel Imputation',method:'Spherical spline interpolation',finding:'< 2% accuracy loss with 1 missing',category:'Hardware'},
    {name:'Class Imbalance Sensitivity',method:'Vary SMOTE ratio (0.5x - 2x)',finding:'Optimal at 1:1 ratio',category:'Data'},
    {name:'Cross-Population',method:'Multi-site generalization',finding:'< 4% variance across sites',category:'Generalization'},
    {name:'Noise Injection',method:'+5%, +10%, +20% SNR degradation',finding:'Robust to +10% noise',category:'Robustness'},
    {name:'Window Size Sensitivity',method:'1s, 2s, 4s, 8s epoch lengths',finding:'4s optimal (accuracy-resolution trade)',category:'Parameter'}
  ],
  validation:[
    {name:'Stratified k-Fold CV (k=10)',purpose:'Balanced class representation across folds'},
    {name:'LOSO Cross-Validation',purpose:'Subject-independent generalization'},
    {name:'Nested Cross-Validation',purpose:'Unbiased hyperparameter tuning'},
    {name:'Bootstrap Resampling (n=1000)',purpose:'Non-parametric confidence intervals'},
    {name:'Holdout Test Set (20%)',purpose:'Final unbiased performance estimate'},
    {name:'External Validation',purpose:'Independent dataset evaluation'},
    {name:'Temporal Split Validation',purpose:'Train on past, test on future'},
    {name:'Multi-Site Validation',purpose:'Cross-institutional generalization'}
  ]
};

// ===== EMOTIV DEVICE DATA =====
const emotivDevices = [
  {name:'Emotiv Insight',channels:5,price:'$299',battery:'8 hrs',sampling:'128 Hz',weight:'115g',connectivity:'BLE 4.0',electrodes:'Semi-dry polymer',color:'#4CAF50',
   positions:['AF3','AF4','T7','T8','Pz(ref)'],
   useCases:['Stress monitoring','Meditation','Attention tracking','Basic wellness'],
   diseases:['Stress'],accuracy:'85-90%'},
  {name:'Emotiv EPOC X',channels:14,price:'$849',battery:'12 hrs',sampling:'128/256 Hz',weight:'380g',connectivity:'BLE 5.0 + USB',electrodes:'Saline felt pads',color:'#2196F3',
   positions:['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4'],
   useCases:['Research-grade diagnosis','Multi-domain screening','PD detection','ASD screening','BCI applications'],
   diseases:['ASD','PD','Stress'],accuracy:'92-97%'},
  {name:'Emotiv EPOC Flex',channels:32,price:'$1,699+',battery:'9 hrs',sampling:'128/256/512 Hz',weight:'Varies',connectivity:'BLE 5.0 + USB',electrodes:'Gel/saline (configurable)',color:'#FF9800',
   positions:['Full 10-20 + 10-10 extensions'],
   useCases:['Clinical-grade diagnosis','Epilepsy monitoring','Depression assessment','Full research studies'],
   diseases:['All 5 diseases'],accuracy:'97-100%'},
  {name:'Emotiv MN8',channels:2,price:'$499',battery:'8 hrs',sampling:'128 Hz',weight:'7.2g (each)',connectivity:'BLE 5.0',electrodes:'In-ear sensors',color:'#9C27B0',
   positions:['In-ear (TP9, TP10 equivalent)'],
   useCases:['Workplace focus','Fatigue detection','Safety monitoring','Discreet wearable'],
   diseases:['Stress'],accuracy:'78-85%'}
];

// ===== ADMIN CONFIG =====
const ADMIN_CREDENTIALS = {username:'admin',passwordHash:'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'};
// SHA-256 of 'admin' — change in production
