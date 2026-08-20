import os
import json
from typing import List, Dict, Any, Optional

# Rich MSMARCO-XI style seed dataset using the ACTUAL schema from ai4bharat/MSMARCO-XI
# Schema: query, Eng_Query, passages.is_selected (list), passages.Translated_passages (list),
#         passages.English_passages (list), Answer, Eng_Answer, query_type, source_lang, target_lang
SEED_DATASET = [
    {
        "query_id": 101,
        "query": "गोवा में घूमने के लिए सबसे अच्छे समुद्र तट कौन से हैं?",
        "Eng_Query": "What are the best beaches to visit in Goa?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "travel",
        "passages": {
            "is_selected": [1, 1, 0],
            "English_passages": [
                "Goa is renowned for its scenic coastline. In North Goa, Baga, Calangute, and Anjuna are popular for nightlife, water sports, and beach shacks. South Goa offers quieter beaches like Palolem, Agonda, and Benaulim, perfect for relaxation and dolphin spotting.",
                "The beaches of Goa attract millions of tourists every year. Baga beach is famous for its vibrant nightlife and water sports activities. Calangute is the longest beach in Goa and is also known as the Queen of Beaches.",
                "Goa has many historic churches and temples dating back to Portuguese colonial rule."
            ],
            "Translated_passages": [
                "गोवा अपने सुंदर समुद्र तटों के लिए प्रसिद्ध है। उत्तर गोवा में बागा, कलंगूट और अंजुना नाइटलाइफ और वाटर स्पोर्ट्स के लिए लोकप्रिय हैं।",
                "गोवा के समुद्र तट हर साल लाखों पर्यटकों को आकर्षित करते हैं। बागा बीच अपनी जीवंत नाइटलाइफ के लिए प्रसिद्ध है।",
                "गोवा में पुर्तगाली शासन काल के कई ऐतिहासिक चर्च और मंदिर हैं।"
            ]
        },
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
        "passages": {
            "is_selected": [1, 1, 0],
            "English_passages": [
                "Dudhsagar Falls is a four-tiered waterfall located on the Mandovi River in the Indian state of Goa. It is 310 metres (1017 feet) tall and has an average width of 30 metres (100 feet). It is one of India's tallest waterfalls.",
                "Dudhsagar, which means 'sea of milk' in Konkani, is located on the Goa-Karnataka border. The waterfall is accessible by jeep safari from Mollem or by train on the Konkan Railway route.",
                "The Mandovi River is the most important river in Goa, flowing westward into the Arabian Sea."
            ],
            "Translated_passages": [
                "दूधसागर जलप्रपात गोवा में मांडवी नदी पर स्थित है। इसकी कुल ऊँचाई लगभग 310 मीटर (1017 फीट) है।",
                "दूधसागर, जिसका अर्थ 'दूध का सागर' है, गोवा-कर्नाटक सीमा पर स्थित है।",
                "मांडवी नदी गोवा की सबसे महत्वपूर्ण नदी है।"
            ]
        },
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
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Hacker House Goa 2026 is an elite developer residency and hackathon in Goa, India, bringing together top builders to build high-performance AI systems, voice agents, and real-time retrieval-augmented generation architectures.",
                "Hacker House Goa is a competitive AI hackathon where participants build voice-enabled RAG systems using datasets like MSMARCO-XI and technologies like FAISS, Sarvam AI STT, and Gemini Flash."
            ],
            "Translated_passages": [
                "हैकर्स हाउस गोवा 2026 एक उच्च-स्तरीय डेवलपर रेजिडेंसी कार्यक्रम है जहाँ एआई, वॉइस RAG पर काम किया जाता है।",
                "हैकर्स हाउस गोवा एक प्रतिस्पर्धी एआई हैकाथॉन है जहाँ वॉइस-इनेबल्ड आरएजी सिस्टम बनाए जाते हैं।"
            ]
        },
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
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "FAISS (Facebook AI Similarity Search) is an open-source library for efficient similarity search and dense vector clustering. In RAG systems, FAISS enables sub-50ms top-k retrieval of passage embeddings matching the query embedding.",
                "In Retrieval-Augmented Generation, FAISS serves as the vector database that stores encoded document embeddings and enables millisecond-speed nearest-neighbor search to find the most relevant context passages for a given query."
            ],
            "Translated_passages": [
                "FAISS डेंस वेक्टर्स की तेज खोज के लिए एक लाइब्रेरी है, जो RAG में 50ms से भी कम समय में प्रासंगिक संदर्भ खोजने की अनुमति देती है।",
                "RAG में FAISS वेक्टर डेटाबेस का काम करता है जो एन्कोडेड दस्तावेज़ एम्बेडिंग संग्रहीत करता है।"
            ]
        },
        "Answer": "FAISS का उपयोग RAG पाइपलाइन में उच्च गति (sub-50ms) वेक्टर समानता खोज के लिए होता है।",
        "Eng_Answer": "FAISS is used in RAG for ultra-fast dense vector similarity search to retrieve relevant context in under 50ms."
    },
    {
        "query_id": 105,
        "query": "सरवम एआई (Sarvam AI) क्या है?",
        "Eng_Query": "What is Sarvam AI and what languages does it support?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Sarvam AI is an Indian artificial intelligence company developing foundational speech-to-text, text-to-speech, and language models specifically optimized for 22 Indian languages including Hindi, Tamil, Telugu, and Marathi.",
                "Sarvam AI's Saaras speech-to-text model supports real-time transcription of spoken Indian languages with high accuracy, making it ideal for voice-enabled AI applications targeting Indian users."
            ],
            "Translated_passages": [
                "सरवम एआई एक भारतीय एआई स्टार्टअप है जो 22 भारतीय भाषाओं के लिए विशेष STT, TTS और भाषा मॉडल बनाता है।",
                "सरवम एआई का सारस STT मॉडल भारतीय भाषाओं की रियल-टाइम ट्रांसक्रिप्शन करता है।"
            ]
        },
        "Answer": "सरवम एआई भारतीय भाषाओं के लिए वॉइस व एलएलएम मॉडल विकसित करने वाली एक एआई कंपनी है।",
        "Eng_Answer": "Sarvam AI is an Indian generative AI company specializing in STT, TTS, and Indic language foundation models for 22 Indian languages."
    },
    {
        "query_id": 106,
        "query": "भारतीय संविधान कब लागू हुआ था?",
        "Eng_Query": "When did the Constitution of India come into effect?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "history",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "The Constitution of India came into effect on 26 January 1950, replacing the Government of India Act 1935 as the country's fundamental governing document. This day is celebrated annually as Republic Day in India.",
                "Dr. B.R. Ambedkar was the principal architect of the Indian Constitution. The Constituent Assembly took nearly three years to draft and finalize the Constitution, which was adopted on 26 November 1949."
            ],
            "Translated_passages": [
                "भारत का संविधान 26 जनवरी 1950 को लागू हुआ था। इस उपलक्ष्य में प्रत्येक वर्ष 26 जनवरी को गणतंत्र दिवस मनाया जाता है।",
                "डॉ. बी.आर. अंबेडकर भारतीय संविधान के प्रमुख निर्माता थे।"
            ]
        },
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
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Photosynthesis is a biological process used by plants, algae, and certain bacteria to convert sunlight, carbon dioxide, and water into chemical energy stored in glucose, releasing oxygen as a byproduct.",
                "The process of photosynthesis occurs in the chloroplasts of plant cells, specifically using chlorophyll to absorb light energy. The overall equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2."
            ],
            "Translated_passages": [
                "प्रकाश संश्लेषण वह प्रक्रिया है जिसके द्वारा हरे पौधे सूर्य के प्रकाश से भोजन (ग्लूकोज) बनाते हैं और ऑक्सीजन छोड़ते हैं।",
                "प्रकाश संश्लेषण पौधों के क्लोरोप्लास्ट में होता है जहाँ क्लोरोफिल प्रकाश ऊर्जा को अवशोषित करता है।"
            ]
        },
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
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "The Taj Mahal is an ivory-white marble mausoleum on the south bank of the Yamuna river in Agra, India. It was commissioned in 1631 by the Mughal emperor Shah Jahan to house the tomb of his favourite wife, Mumtaz Mahal.",
                "The Taj Mahal was built between 1632 and 1653 and employed over 20,000 artisans. It is considered one of the finest examples of Mughal architecture and a UNESCO World Heritage Site."
            ],
            "Translated_passages": [
                "ताजमहल आगरा में स्थित एक सफेद संगमरमर का मकबरा है जिसे मुगल सम्राट शाहजहाँ ने अपनी प्रिय बेगम मुमताज महल की याद में बनवाया था।",
                "ताजमहल 1632 से 1653 के बीच बनाया गया था और यह यूनेस्को विश्व धरोहर स्थल है।"
            ]
        },
        "Answer": "ताजमहल मुगल सम्राट शाहजहाँ ने अपनी बेगम मुमताज महल की याद में बनवाया था।",
        "Eng_Answer": "The Taj Mahal was commissioned by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal."
    },
    {
        "query_id": 109,
        "query": "विराट कोहली कौन हैं और उन्होंने क्रिकेट में क्या उपलब्धियां हासिल की हैं?",
        "Eng_Query": "Who is Virat Kohli and what are his cricket achievements?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "sports",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Virat Kohli is an Indian international cricketer who is regarded as one of the greatest batsmen of all time. He has scored over 26,000 international runs across all formats and holds numerous batting records including most ODI centuries after Sachin Tendulkar.",
                "Virat Kohli captained the Indian national cricket team in Test, ODI, and T20I formats. He is known for his aggressive batting style and exceptional fitness. He has scored over 80 international centuries and is considered one of the best batsmen in the world."
            ],
            "Translated_passages": [
                "विराट कोहली एक भारतीय अंतरराष्ट्रीय क्रिकेटर हैं जिन्हें सर्वकालिक महान बल्लेबाजों में से एक माना जाता है।",
                "विराट कोहली ने भारतीय क्रिकेट टीम की कप्तानी की है और उन्होंने 80 से अधिक अंतरराष्ट्रीय शतक लगाए हैं।"
            ]
        },
        "Answer": "विराट कोहली एक महान भारतीय बल्लेबाज हैं जिन्होंने अंतरराष्ट्रीय क्रिकेट में 80 से अधिक शतक और 26,000 से अधिक रन बनाए हैं।",
        "Eng_Answer": "Virat Kohli is one of the greatest Indian cricketers with over 80 international centuries and 26,000+ runs across all formats."
    },
    {
        "query_id": 110,
        "query": "आर्टिफिशियल इंटेलिजेंस क्या है?",
        "Eng_Query": "What is Artificial Intelligence?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Artificial Intelligence (AI) is the simulation of human intelligence processes by computer systems. These processes include learning (acquiring information and rules for using it), reasoning (using rules to reach approximate or definite conclusions), and self-correction.",
                "Modern AI includes machine learning, deep learning, natural language processing, and computer vision. Large language models (LLMs) like GPT and Gemini represent the latest advancement in AI, capable of understanding and generating human-like text."
            ],
            "Translated_passages": [
                "आर्टिफिशियल इंटेलिजेंस (AI) कंप्यूटर सिस्टम द्वारा मानव बुद्धिमत्ता की नकल करने की प्रक्रिया है।",
                "आधुनिक AI में मशीन लर्निंग, डीप लर्निंग और प्राकृतिक भाषा प्रसंस्करण शामिल हैं।"
            ]
        },
        "Answer": "आर्टिफिशियल इंटेलिजेंस कंप्यूटर सिस्टम में मानवीय बुद्धिमत्ता का अनुकरण है जिसमें सीखना, तर्क करना और स्वयं सुधार करना शामिल है।",
        "Eng_Answer": "Artificial Intelligence is the simulation of human intelligence by computer systems including learning, reasoning, and self-correction."
    },
    {
        "query_id": 111,
        "query": "क्रिकेट विश्व कप 2023 किसने जीता?",
        "Eng_Query": "Who won the Cricket World Cup 2023?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "sports",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "Australia won the ICC Cricket World Cup 2023, defeating India in the final held at the Narendra Modi Stadium in Ahmedabad on November 19, 2023. This was Australia's sixth World Cup title.",
                "The ICC Men's Cricket World Cup 2023 was hosted by India. India reached the final unbeaten but were defeated by Australia by 6 wickets. Travis Head scored a brilliant century to help Australia win."
            ],
            "Translated_passages": [
                "ऑस्ट्रेलिया ने 2023 आईसीसी क्रिकेट विश्व कप जीता, अहमदाबाद में फाइनल में भारत को हराकर।",
                "2023 विश्व कप का फाइनल अहमदाबाद के नरेंद्र मोदी स्टेडियम में खेला गया जहाँ ट्रैविस हेड की शानदार शतकीय पारी से ऑस्ट्रेलिया ने जीत हासिल की।"
            ]
        },
        "Answer": "ऑस्ट्रेलिया ने 2023 आईसीसी क्रिकेट विश्व कप जीता, फाइनल में भारत को हराकर।",
        "Eng_Answer": "Australia won the ICC Cricket World Cup 2023, defeating India in the final at Ahmedabad."
    },
    {
        "query_id": 112,
        "query": "भारत की राजधानी क्या है?",
        "Eng_Query": "What is the capital of India?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "geography",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "New Delhi is the capital of India and serves as the seat of all three branches of the Government of India — the executive, the legislative, and the judiciary. It is located within the National Capital Territory of Delhi.",
                "New Delhi was designed by British architects Edwin Lutyens and Herbert Baker and was inaugurated as the capital of British India in 1931. It replaced Calcutta (now Kolkata) as the administrative capital."
            ],
            "Translated_passages": [
                "नई दिल्ली भारत की राजधानी है और भारत सरकार की कार्यपालिका, विधायिका और न्यायपालिका का केंद्र है।",
                "नई दिल्ली को ब्रिटिश वास्तुकारों एडविन लुटियंस और हर्बर्ट बेकर द्वारा डिजाइन किया गया था।"
            ]
        },
        "Answer": "भारत की राजधानी नई दिल्ली है।",
        "Eng_Answer": "The capital of India is New Delhi."
    },
    {
        "query_id": 113,
        "query": "MS MARCO XI डेटासेट क्या है?",
        "Eng_Query": "What is the MSMARCO-XI dataset?",
        "source_lang": "eng_Latn",
        "target_lang": "hin_Deva",
        "query_type": "technology",
        "passages": {
            "is_selected": [1, 1],
            "English_passages": [
                "MSMARCO-XI (IndicRAGSuite) is a dataset by AI4Bharat containing the MS MARCO dataset translated into 14 Indic languages including Hindi, Bengali, Tamil, Telugu, Marathi, and more. It contains over 10 million training rows for multilingual retrieval-augmented generation research.",
                "The ai4bharat/MSMARCO-XI dataset is available on HuggingFace and supports languages like Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Nepali, Odia, Punjabi, Sanskrit, Tamil, Telugu, and Urdu. It is used for building Indic language RAG systems."
            ],
            "Translated_passages": [
                "MSMARCO-XI एक AI4Bharat का डेटासेट है जिसमें MS MARCO को 14 भारतीय भाषाओं में अनुवादित किया गया है।",
                "ai4bharat/MSMARCO-XI HuggingFace पर उपलब्ध है और हिंदी, बंगाली, तमिल सहित कई भाषाओं का समर्थन करता है।"
            ]
        },
        "Answer": "MSMARCO-XI AI4Bharat द्वारा बनाया गया एक बहुभाषी डेटासेट है जिसमें 14 भारतीय भाषाओं में MS MARCO के अनुवाद शामिल हैं।",
        "Eng_Answer": "MSMARCO-XI is a multilingual dataset by AI4Bharat containing MS MARCO translated into 14 Indic languages for RAG research."
    }
]


def _normalize_record(record: Dict[str, Any], idx: int) -> Dict[str, Any]:
    """
    Normalize a raw HuggingFace MSMARCO-XI record OR a seed dataset record 
    into a consistent internal format with flat passage list.
    Handles both schema versions:
    - HF schema: passages.is_selected (list), passages.English_passages (list), passages.Translated_passages (list)
    - Legacy seed: passages as list of dicts with passage_text
    """
    passages_raw = record.get("passages", {})
    flat_passages = []

    if isinstance(passages_raw, dict):
        # Real MSMARCO-XI HuggingFace schema
        en_passages = passages_raw.get("English_passages", [])
        tr_passages = passages_raw.get("Translated_passages", [])
        is_selected = passages_raw.get("is_selected", [])

        for i, (ep, is_sel) in enumerate(zip(en_passages, is_selected)):
            flat_passages.append({
                "passage_text": ep,
                "is_selected": int(is_sel),
                "lang": "en",
                "url": ""
            })
            # Also add translated passage if available
            if i < len(tr_passages) and tr_passages[i]:
                flat_passages.append({
                    "passage_text": tr_passages[i],
                    "is_selected": int(is_sel),
                    "lang": record.get("target_lang", "hin_Deva"),
                    "url": ""
                })
    elif isinstance(passages_raw, list):
        # Legacy seed dataset schema
        for p in passages_raw:
            if isinstance(p, dict):
                flat_passages.append({
                    "passage_text": p.get("passage_text", ""),
                    "is_selected": p.get("is_selected", 0),
                    "lang": "en",
                    "url": p.get("url", "")
                })

    return {
        "query_id": record.get("query_id", f"doc_{idx}"),
        "query": record.get("query", ""),
        "Eng_Query": record.get("Eng_Query", record.get("query", "")),
        "query_type": record.get("query_type", "general"),
        "source_lang": record.get("source_lang", "eng_Latn"),
        "target_lang": record.get("target_lang", "hin_Deva"),
        "passages": flat_passages,
        "Answer": record.get("Answer", ""),
        "Eng_Answer": record.get("Eng_Answer", "")
    }


def load_msmarco_xi_dataset(max_samples: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Loads dataset records using the real ai4bharat/MSMARCO-XI schema.
    Tries HuggingFace first, falls back to curated seed dataset.
    """
    try:
        from datasets import load_dataset
        print("Attempting to load ai4bharat/MSMARCO-XI from HuggingFace...")
        ds = load_dataset("ai4bharat/MSMARCO-XI", "hi", split="validation", streaming=True)
        records = []
        for i, row in enumerate(ds):
            if max_samples and i >= max_samples:
                break
            records.append(_normalize_record(row, i))
        if records:
            print(f"Loaded {len(records)} records from HuggingFace MSMARCO-XI.")
            return records
    except Exception as e:
        print(f"HuggingFace dataset direct load notice ({e}). Using embedded seed dataset.")

    # Use rich seed dataset with normalized format
    normalized = [_normalize_record(r, i) for i, r in enumerate(SEED_DATASET)]
    return normalized[:max_samples] if max_samples else normalized
