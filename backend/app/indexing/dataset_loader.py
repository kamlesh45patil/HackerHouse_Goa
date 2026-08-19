import os
import json
from typing import List, Dict, Any, Optional

# Sample rich dataset of MSMARCO-XI style English & Indic (Hindi/Hinglish) QA passages
SEED_DATASET = [
    {
        "query_id": 101,
        "query": "गोवा में घूमने के लिए सबसे अच्छे समुद्र तट कौन से हैं?",
        "Eng_Query": "What are the best beaches to visit in Goa?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "travel",
        "passages": [
            {
                "passage_text": "Goa is renowned for its scenic coastline. In North Goa, Baga, Calangute, and Anjuna are popular for nightlife, water sports, and beach shacks. South Goa offers quieter beaches like Palolem, Agonda, and Benaulim, perfect for relaxation and dolphin spotting.",
                "is_selected": 1,
                "url": "https://goatourism.gov.in/beaches"
            },
            {
                "passage_text": "उत्तर गोवा में बागा और कलंगूट समुद्र तट अपने वाटर स्पोर्ट्स, नाइटलाइफ़ और कैफ़े के लिए प्रसिद्ध हैं। दक्षिण गोवा में पालोलेम और अगोंडा शांत और सुंदर दृश्यों के लिए जाने जाते हैं।",
                "is_selected": 1,
                "url": "https://goatourism.gov.in/hi/beaches"
            },
            {
                "passage_text": "The Dudhsagar Falls is a four-tiered waterfall located on the Mandovi River in Goa. It is 60 km from Panaji on the Madgaon-Belagavi rail route.",
                "is_selected": 0,
                "url": "https://en.wikipedia.org/wiki/Dudhsagar_Falls"
            }
        ],
        "Answer": "गोवा में घूमने के लिए उत्तर गोवा में बागा, कलंगूट और अंजुना तथा दक्षिण गोवा में पालोलेम और अगोंडा प्रमुख समुद्र तट हैं।",
        "Eng_Answer": "The top beaches in Goa are Baga, Calangute, and Anjuna in North Goa, and Palolem and Agonda in South Goa."
    },
    {
        "query_id": 102,
        "query": "दूधसागर जलप्रपात कहाँ स्थित है और इसकी ऊँचाई कितनी है?",
        "Eng_Query": "Where is Dudhsagar Falls located and what is its height?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "geography",
        "passages": [
            {
                "passage_text": "Dudhsagar Falls is a four-tiered waterfall located on the Mandovi River in the Indian state of Goa. It is 310 metres (1017 feet) tall and has an average width of 30 metres (100 feet). It is one of India's tallest waterfalls.",
                "is_selected": 1,
                "url": "https://en.wikipedia.org/wiki/Dudhsagar_Falls"
            },
            {
                "passage_text": "दूधसागर जलप्रपात गोवा में मांडवी नदी पर स्थित है। इसकी कुल ऊँचाई लगभग 310 मीटर (1017 फीट) है और यह भारत के सबसे ऊँचे झरनों में से एक है।",
                "is_selected": 1,
                "url": "https://hi.wikipedia.org/wiki/दूधसागर_जलप्रपात"
            }
        ],
        "Answer": "दूधसागर जलप्रपात गोवा में मांडवी नदी पर स्थित है और इसकी ऊँचाई लगभग 310 मीटर (1017 फीट) है।",
        "Eng_Answer": "Dudhsagar Falls is located on the Mandovi River in Goa with a height of 310 meters (1017 feet)."
    },
    {
        "query_id": 103,
        "query": "हैकर्स हाउस गोवा 2026 क्या है?",
        "Eng_Query": "What is Hacker House Goa 2026?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": [
            {
                "passage_text": "Hacker House Goa 2026 is an elite developer residency and hackathon in Goa, India, bringing together top builders to build high-performance AI systems, voice agents, and real-time retrieval-augmented generation architectures.",
                "is_selected": 1,
                "url": "https://hackerhousegoa.dev"
            },
            {
                "passage_text": "हैकर्स हाउस गोवा 2026 एक उच्च-स्तरीय डेवलपर रेजिडेंसी कार्यक्रम है जहाँ एआई, वॉइस-इनेबल्ड आरएजी (Voice RAG), और रियल-टाइम आर्किटेक्चर पर काम किया जाता है।",
                "is_selected": 1,
                "url": "https://hackerhousegoa.dev/hi"
            }
        ],
        "Answer": "हैकर्स हाउस गोवा 2026 शीर्ष डेवलपर्स के लिए एक एआई और आरएजी नवाचार रेजिडेंसी है।",
        "Eng_Answer": "Hacker House Goa 2026 is an AI builder residency and hackathon focused on real-time systems and voice RAG."
    },
    {
        "query_id": 104,
        "query": "RAG सिस्टम में FAISS का क्या उपयोग है?",
        "Eng_Query": "What is the role of FAISS in a RAG system?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": [
            {
                "passage_text": "FAISS (Facebook AI Similarity Search) is an open-source library for efficient similarity search and dense vector clustering. In RAG systems, FAISS enables sub-50ms top-k retrieval of passage embeddings matching the query embedding.",
                "is_selected": 1,
                "url": "https://github.com/facebookresearch/faiss"
            },
            {
                "passage_text": "एफएआईएसएस (FAISS) डेंस वेक्टर्स की तेज खोज के लिए एक लाइब्रेरी है, जो आरएजी में 50 मिलीसेकंड से भी कम समय में प्रासंगिक संदर्भ खोजने की अनुमति देती है।",
                "is_selected": 1,
                "url": "https://faiss.ai/hi"
            }
        ],
        "Answer": "FAISS का उपयोग आरएजी पाइपलाइन में उच्च गति (sub-50ms) से वेक्टर समानता खोज और प्रासंगिक अंश निकालने के लिए होता है।",
        "Eng_Answer": "FAISS is used in RAG for ultra-fast dense vector similarity search to retrieve relevant context in under 50ms."
    },
    {
        "query_id": 105,
        "query": "सरवम एआई (Sarvam AI) क्या है?",
        "Eng_Query": "What is Sarvam AI?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": [
            {
                "passage_text": "Sarvam AI is an Indian artificial intelligence company developing foundational speech-to-text, text-to-speech, and language models specifically optimized for 22 Indian languages including Hindi, Tamil, Telugu, and Marathi.",
                "is_selected": 1,
                "url": "https://www.sarvam.ai"
            },
            {
                "passage_text": "सरवम एआई एक भारतीय एआई स्टार्टअप है जो 22 भारतीय भाषाओं के लिए विशेष स्पीच-टू-टेक्स्ट (STT), टीटीएस और भाषा मॉडल बनाता है।",
                "is_selected": 1,
                "url": "https://www.sarvam.ai/hi"
            }
        ],
        "Answer": "सरवम एआई भारतीय भाषाओं के लिए वॉइस व एलएलएम मॉडल विकसित करने वाली एक एआई कंपनी है।",
        "Eng_Answer": "Sarvam AI is an Indian generative AI company specializing in STT, TTS, and Indic language foundation models."
    },
    {
        "query_id": 106,
        "query": "भारतीय संविधान कब लागू हुआ था?",
        "Eng_Query": "When did the Constitution of India come into effect?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "history",
        "passages": [
            {
                "passage_text": "The Constitution of India came into effect on 26 January 1950, replacing the Government of India Act 1935 as the country's fundamental governing document. This day is celebrated annually as Republic Day in India.",
                "is_selected": 1,
                "url": "https://en.wikipedia.org/wiki/Constitution_of_India"
            },
            {
                "passage_text": "भारत का संविधान 26 जनवरी 1950 को लागू हुआ था। इस उपलक्ष्य में प्रत्येक वर्ष 26 जनवरी को गणतंत्र दिवस मनाया जाता है।",
                "is_selected": 1,
                "url": "https://hi.wikipedia.org/wiki/भारत_का_संविधान"
            }
        ],
        "Answer": "भारतीय संविधान 26 जनवरी 1950 को लागू हुआ था।",
        "Eng_Answer": "The Constitution of India came into effect on January 26, 1950."
    },
    {
        "query_id": 107,
        "query": "फोटोसिंथेसिस (प्रकाश संश्लेषण) क्या है?",
        "Eng_Query": "What is photosynthesis?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "science",
        "passages": [
            {
                "passage_text": "Photosynthesis is a biological process used by plants, algae, and certain bacteria to convert sunlight, carbon dioxide, and water into chemical energy stored in glucose, releasing oxygen as a byproduct.",
                "is_selected": 1,
                "url": "https://en.wikipedia.org/wiki/Photosynthesis"
            },
            {
                "passage_text": "प्रकाश संश्लेषण वह प्रक्रिया है जिसके द्वारा हरे पौधे सूर्य के प्रकाश, पानी और कार्बन डाइऑक्साइड का उपयोग करके अपना भोजन (ग्लूकोज) बनाते हैं और ऑक्सीजन छोड़ते हैं।",
                "is_selected": 1,
                "url": "https://hi.wikipedia.org/wiki/प्रकाश_संश्लेषण"
            }
        ],
        "Answer": "प्रकाश संश्लेषण पौधों द्वारा सूर्य के प्रकाश से भोजन और ऑक्सीजन बनाने की प्रक्रिया है।",
        "Eng_Answer": "Photosynthesis is the process by which green plants use sunlight, CO2, and water to synthesize glucose and produce oxygen."
    },
    {
        "query_id": 108,
        "query": "ताजमहल किसने और किसकी याद में बनवाया था?",
        "Eng_Query": "Who built the Taj Mahal and in whose memory?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "history",
        "passages": [
            {
                "passage_text": "The Taj Mahal is an ivory-white marble mausoleum on the south bank of the Yamuna river in Agra, India. It was commissioned in 1631 by the Mughal emperor Shah Jahan to house the tomb of his favourite wife, Mumtaz Mahal.",
                "is_selected": 1,
                "url": "https://en.wikipedia.org/wiki/Taj_Mahal"
            },
            {
                "passage_text": "ताजमहल आगरा में स्थित एक सफेद संगमरमर का मकबरा है जिसे मुगल सम्राट शाहजहाँ ने अपनी प्रिय बेगम मुमताज महल की याद में बनवाया था।",
                "is_selected": 1,
                "url": "https://hi.wikipedia.org/wiki/ताजमहल"
            }
        ],
        "Answer": "ताजमहल मुगल सम्राट शाहजहाँ ने अपनी बेगम मुमताज महल की याद में बनवाया था।",
        "Eng_Answer": "The Taj Mahal was commissioned by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal."
    }
]

def load_msmarco_xi_dataset(max_samples: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Loads dataset records. Uses HuggingFace datasets if installed and online,
    otherwise loads the curated multilingual Indic benchmark dataset.
    """
    try:
        from datasets import load_dataset
        print("Attempting to load ai4bharat/MSMARCO-XI from HuggingFace...")
        # Stream a slice for fast startup
        ds = load_dataset("ai4bharat/MSMARCO-XI", "hi", split="validation", streaming=True)
        records = []
        for i, row in enumerate(ds):
            if max_samples and i >= max_samples:
                break
            records.append(row)
        if records:
            print(f"Loaded {len(records)} records from HuggingFace MSMARCO-XI.")
            return records
    except Exception as e:
        print(f"HuggingFace dataset direct load notice ({e}). Using embedded seed dataset.")
    
    return SEED_DATASET[:max_samples] if max_samples else SEED_DATASET
