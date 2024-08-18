import streamlit as st
import openai
#import json
import os

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use the new model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Translate the following English text to French: 'Hello, how are you?'"},
    ]
)
print(response['choices'][0]['message']['content'])


# Syllabus for Tingkatan 4 and 5
syllabus = {
    "Tingkatan 4": [
        "Warisan Negara Bangsa",
        "Kebangkitan Nasionalisme",
        "Konflik Dunia dan Pendudukan Jepun di Negara Kita",
        "Era Peralihan Kuasa British di Negara Kita",
        "Persekutuan Tanah Melayu 1948",
        "Ancaman Komunis dan Perisytiharan Darurat",
        "Usaha ke Arah Kemerdekaan",
        "Pilihan Raya",
        "Perlembagaan Persekutuan Tanah Melayu 1957",
        "Pemasyhuran Kemerdekaan"
    ],
    "Tingkatan 5": [
        "Kedaulatan Negara",
        "Perlembagaan Persekutuan",
        "Raja Berperlembagaan dan Demokrasi Berparlimen",
        "Sistem Persekutuan",
        "Pembentukan Malaysia",
        "Cabaran Selepas Pembentukan Malaysia",
        "Membina Kesejahteraan Negara",
        "Membina Kemakmuran Negara",
        "Dasar Luar Malaysia",
        "Kecemerlangan Malaysia di Persada Dunia"
    ]
}

# Sidebar for selecting form and topics
st.sidebar.header("Pilih Tingkatan")
selected_form = st.sidebar.selectbox("Tingkatan", list(syllabus.keys()))
selected_topic = st.sidebar.selectbox("Topik", syllabus[selected_form])

# Main panel
st.title("Pembantu Sejarah SPM")
st.header("Penjelasan Topik")
st.write(f"Topik yang dipilih: {selected_topic}")

# Explanation button
if st.button("Terangkan Topik"):
    prompt = f"Terangkan secara mendalam mengenai {selected_topic} dalam konteks Sejarah SPM."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Anda adalah seorang guru Sejarah yang berpengalaman."},
            {"role": "user", "content": prompt}
        ]
    )
    st.write(response.choices[0].message['content'])

# Objective questions button
st.header("Soalan Objektif")

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.correct_answers = {}

if st.button("Hasilkan Soalan Objektif"):
    prompt = (
        f"Sila jana 5 soalan objektif dengan 4 pilihan jawapan mengenai topik '{selected_topic}'. "
        f"Setiap soalan hendaklah disusun seperti berikut:\n"
        f"1. Soalan: <soalan>\n"
        f"A) <jawapan 1>\n"
        f"B) <jawapan 2>\n"
        f"C) <jawapan 3>\n"
        f"D) <jawapan 4>\n"
        f"Jawapan yang betul: <jawapan yang betul>"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Anda adalah seorang guru Sejarah yang berpengalaman."},
            {"role": "user", "content": prompt}
        ]
    )

    questions = response.choices[0].message['content'].split('\n\n')

    st.session_state.questions = []
    st.session_state.correct_answers = {}

    for i, question_block in enumerate(questions, start=1):
        lines = [line.strip() for line in question_block.split('\n') if line.strip()]
        if len(lines) >= 6:  # Ensure there are 4 options and a correct answer
            question_text = lines[0]
            options = lines[1:5]
            correct_answer = lines[-1].replace("Jawapan yang betul:", "").strip()

            if correct_answer in options:
                st.session_state.questions.append((question_text, options))
                st.session_state.correct_answers[i] = correct_answer
            else:
                st.error(f"Soalan {i} tidak mempunyai jawapan yang betul yang ditandai dengan jelas. Sila jana semula.")
                break

# Display objective questions if they exist
if st.session_state.questions:
    for i, (question_text, options) in enumerate(st.session_state.questions, start=1):
        st.subheader(f"Soalan {i}")
        st.write(question_text)
        chosen_answer = st.radio(f"Jawapan untuk soalan {i}:", options, key=f"q{i}")
        st.session_state[f"selected_answer_{i}"] = chosen_answer

# Check objective answers button
if st.session_state.questions and st.button("Semak Jawapan"):
    st.header("Keputusan Semakan")
    correct_count = 0
    for i in range(1, len(st.session_state.questions) + 1):
        selected_answer = st.session_state.get(f"selected_answer_{i}")
        correct_answer = st.session_state.correct_answers.get(i)
        if selected_answer:
            if selected_answer == correct_answer:
                st.write(f"Soalan {i}: Betul! Anda memilih '{selected_answer}'")
                correct_count += 1
            else:
                st.write(f"Soalan {i}: Salah. Anda memilih '{selected_answer}', jawapan yang betul ialah '{correct_answer}'")
        else:
            st.write(f"Soalan {i}: Tiada jawapan dipilih. Jawapan yang betul ialah '{correct_answer}'")
    st.write(f"Anda mendapat {correct_count} daripada {len(st.session_state.questions)} soalan dengan betul.")

# Subjective questions button
st.header("Soalan Subjektif")

if st.button("Hasilkan Soalan Subjektif"):
    prompt = (
        f"Sila jana 5 soalan subjektif yang berkaitan dengan topik '{selected_topic}' "
        f"untuk pelajar Sejarah SPM. Sertakan jawapan cadangan untuk setiap soalan."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Anda adalah seorang guru Sejarah yang berpengalaman."},
            {"role": "user", "content": prompt}
        ]
    )
    subjective_questions = response.choices[0].message['content'].split('\n\n')

    for i, question_answer in enumerate(subjective_questions[:5], start=1):  # Ensure only 5 questions
        parts = question_answer.split("Jawapan cadangan:")
        if len(parts) == 2:
            question, answer = parts
            st.subheader(f"Soalan {i} Subjektif")
            st.write(question.strip())
            st.markdown(f"**Jawapan Cadangan:** {answer.strip()}")
        else:
            st.subheader(f"Soalan {i} Subjektif")
            st.write(question_answer.strip())
            st.markdown("**Jawapan Cadangan:** Tidak disediakan.")
