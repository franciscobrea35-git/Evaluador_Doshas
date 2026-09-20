from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="Evaluador de Doshas",
    page_icon="🪷",
    layout="centered",
    initial_sidebar_state="collapsed",
)


QUESTIONNAIRES = {
    "Vata": [
        "Realizo mis actividades muy de prisa.",
        "No sirvo para memorizar cosas y recordarlas más adelante.",
        "Soy entusiasta y vivaz por naturaleza.",
        "Soy delgado; no aumento de peso con facilidad.",
        "Siempre he sido rápido para aprender cosas nuevas.",
        "Mi paso característico al caminar es ligero y rápido.",
        "Tiendo a tener dificultades en tomar decisiones.",
        "Suelo tener gases o estreñimiento fácilmente.",
        "Normalmente tengo las manos y los pies fríos.",
        "Me pongo ansioso o me preocupo frecuentemente.",
        "No tolero el frío tanto como la mayoría.",
        "Hablo con rapidez, y mis amigos me consideran parlanchín.",
        "Cambio de humor con facilidad y soy emotivo por naturaleza.",
        "Con frecuencia me cuesta conciliar el sueño o dormir profundamente toda la noche.",
        "Mi piel tiende a ser muy seca, especialmente en invierno.",
        "Mi mente es muy activa, a veces inquieta, pero también muy imaginativa.",
        "Mis movimientos son rápidos y activos; mi energía tiende a surgir como arranques.",
        "Soy fácilmente excitable.",
        "Si de mí depende, mis hábitos de comida y descanso tienden a ser irregulares.",
        "Aprendo con rapidez, pero también olvido con rapidez.",
    ],
    "Pitta": [
        "Me considero muy eficiente.",
        "En mis actividades tiendo a ser sumamente exacto y ordenado.",
        "Soy de carácter firme y tengo una actitud algo enérgica.",
        "Me siento más incómodo o me fatigo con más facilidad cuando hace calor que la mayoría.",
        "Tiendo a transpirar con facilidad.",
        "Aunque no siempre lo demuestre, me irrito o me enojo con facilidad.",
        "Si me salto una comida o esta se retrasa me siento incómodo.",
        "Una o más de las siguientes características corresponden a mi pelo: prematuramente cano o calvo, fino, suave, lacio, rubio, pelirrojo o muy claro.",
        "Tengo buen apetito; si lo deseo, puedo comer en gran cantidad.",
        "Mucha gente me considera terco.",
        "Soy muy regular en mi funcionamiento intestinal; en mí es más común la diarrea que el estreñimiento.",
        "Me impaciento con mucha facilidad.",
        "Tiendo a ser perfeccionista en cuanto a los detalles.",
        "Me enojo con bastante facilidad, pero lo olvido pronto.",
        "Me gustan mucho los alimentos fríos, como el helado y las bebidas heladas.",
        "Si la habitación está demasiado calorosa, lo noto con más facilidad que si está demasiado fría.",
        "No tolero las comidas muy calientes ni muy condimentadas.",
        "No soy tan tolerante como debería con quienes disienten conmigo.",
        "Disfruto con el desafío, y cuando deseo algo soy muy decidido en mis esfuerzos por conseguirlo.",
        "Tiendo a ser muy crítico con los otros y también conmigo mismo.",
    ],
    "Kapha": [
        "Mi tendencia natural es a hacer mis tareas de modo lento y relajado.",
        "Aumento de peso con más facilidad que la mayoría y me cuesta más adelgazar.",
        "Tengo un temperamento plácido y sereno; no me altero con facilidad.",
        "Puedo saltarme comidas sin malestares significativos.",
        "Tiendo a un exceso de moco, flema, congestión crónica, asma o problemas en los senos paranasales.",
        "Debo dormir al menos ocho horas para estar bien al día siguiente.",
        "Duermo muy profundamente.",
        "Soy sereno por naturaleza y difícil de enojar.",
        "No aprendo tan fácilmente como otros, pero tengo excelente retención y larga memoria.",
        "Tiendo a engordar; acumulo grasa con facilidad.",
        "Me molesta el tiempo fresco y húmedo.",
        "Mi pelo es grueso, oscuro y ondeado.",
        "Tengo la piel suave y tez algo pálida.",
        "Mi cuerpo es grande y sólido.",
        "Las siguientes palabras me describen bien: sereno, dulce, afectuoso y con propensión a perdonar.",
        "Tengo digestión lenta, por lo cual me siento pesado después de comer.",
        "Tengo muy buen vigor y resistencia física y un nivel de energía parejo.",
        "Generalmente camino a paso lento y medido.",
        "Tiendo a dormir demasiado, al aturdimiento al despertar y, en general, soy lento para entrar en actividad por la mañana.",
        "Como con lentitud; soy lento y metódico en mis actos.",
    ],
}


DOSHA_INFO = {
    "Vata": {
        "emoji": "🌬️",
        "color": "#7861A8",
        "elements": "espacio y aire",
        "summary": "movimiento, rapidez, creatividad y adaptación",
    },
    "Pitta": {
        "emoji": "🔥",
        "color": "#E36C43",
        "elements": "fuego y agua",
        "summary": "transformación, determinación, precisión y organización",
    },
    "Kapha": {
        "emoji": "🌿",
        "color": "#3D8B6C",
        "elements": "tierra y agua",
        "summary": "estructura, estabilidad, paciencia y resistencia",
    },
}


SCORE_OPTIONS = {
    "1 — No se aplica en absoluto": 1,
    "2 — Casi no se aplica": 2,
    "3 — Se aplica a veces, en menor grado": 3,
    "4 — Se aplica a veces, en mayor grado": 4,
    "5 — Se aplica generalmente": 5,
    "6 — Se aplica casi siempre": 6,
}


def calculate_result(section_scores):
    """Calcula los porcentajes comparativos a partir de los tres totales."""
    grand_total = sum(section_scores.values())
    percentages = {
        dosha: round((score / grand_total) * 100, 1)
        for dosha, score in section_scores.items()
    }
    ranked = sorted(percentages, key=percentages.get, reverse=True)
    gap_first_second = percentages[ranked[0]] - percentages[ranked[1]]
    spread = percentages[ranked[0]] - percentages[ranked[2]]

    if spread <= 5:
        profile = "Tridosha"
        explanation = "Los tres doshas presentan una distribución muy cercana."
    elif gap_first_second <= 5:
        profile = f"{ranked[0]}–{ranked[1]}"
        explanation = f"Predominan dos doshas con puntuaciones cercanas: {ranked[0]} y {ranked[1]}."
    else:
        profile = ranked[0]
        explanation = f"El dosha con mayor puntuación es {ranked[0]}."

    return grand_total, percentages, ranked, profile, explanation


def build_report(name, section_scores, grand_total, percentages, profile, explanation):
    person = name.strip() or "Persona evaluada"
    return f"""EVALUACIÓN DE DOSHAS
Fecha: {datetime.now().strftime('%d/%m/%Y')}
Nombre: {person}

RESULTADO
Perfil: {profile}

Vata:  {section_scores['Vata']} puntos — {percentages['Vata']:.1f}%
Pitta: {section_scores['Pitta']} puntos — {percentages['Pitta']:.1f}%
Kapha: {section_scores['Kapha']} puntos — {percentages['Kapha']:.1f}%
Suma general: {grand_total} puntos

Interpretación: {explanation}

Fórmula utilizada:
Porcentaje del dosha = total del dosha / suma de los tres totales × 100.

Cada sección contiene 20 afirmaciones puntuadas del 1 al 6.
Esta herramienta tiene fines educativos y no constituye diagnóstico médico.
"""


st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #DDF4FA 0%, #F4FBF7 48%, #FFFFFF 100%); }
    .block-container { max-width: 900px; padding-top: 1.5rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #173F4F; }
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #BFE1D4;
        border-radius: 20px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 8px 25px rgba(31, 89, 99, 0.08);
    }
    .hero {
        background: linear-gradient(135deg, #236B73, #3E927B);
        color: white;
        padding: 1.55rem;
        border-radius: 22px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 28px rgba(35, 107, 115, 0.18);
    }
    .hero h1 { color: white; margin: 0; font-size: 2rem; }
    .hero p { margin: .55rem 0 0; opacity: .96; }
    .question-number { color: #236B73; font-weight: 700; margin-top: .45rem; }
    .scale {
        background: #EEF8F3;
        border: 1px solid #C9E7D9;
        border-radius: 14px;
        padding: .75rem .9rem;
        margin: .4rem 0 1rem;
    }
    .result-card {
        background: #FFFFFF !important;
        color: #173F4F !important;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: .45rem 0;
        border-left: 7px solid var(--accent);
        box-shadow: 0 5px 16px rgba(31, 89, 99, 0.08);
    }
    .result-card h3 {
        color: #173F4F !important;
        margin: 0;
    }
    .result-card p, .result-card b {
        color: #173F4F !important;
        margin: .25rem 0 0;
    }
    .notice {
        background: #FFF8E7;
        border: 1px solid #F0D999;
        border-radius: 14px;
        padding: .8rem 1rem;
        color: #5E4B18;
    }
    div[data-baseweb="select"] > div {
        background: linear-gradient(90deg, #1769C2 0%, #A63BD4 55%, #E23CAC 100%) !important;
        border: 1px solid #D45AC1 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    div[data-baseweb="input"] > div {
        background: #EAF4FF !important;
        border: 2px solid #C843C4 !important;
    }
    div[data-baseweb="input"] input {
        background: transparent !important;
        color: #173F4F !important;
    }
    div.stButton > button,
    div.stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #1769C2 0%, #A63BD4 55%, #E23CAC 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        border-radius: 12px;
        font-weight: 700;
        min-height: 3rem;
    }
    div.stButton > button:hover,
    div.stDownloadButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(90deg, #12549D 0%, #8F2DBC 55%, #C92A96 100%) !important;
        color: #FFFFFF !important;
    }
    @media (max-width: 600px) {
        .block-container { padding: .75rem .65rem 2rem; }
        .hero { padding: 1.15rem; border-radius: 17px; }
        .hero h1 { font-size: 1.55rem; }
        [data-testid="stForm"] { padding: .8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <section class="hero">
        <h1>🪷 Evaluador de Doshas</h1>
        <p>Calcula la proporción de Vata, Pitta y Kapha mediante tres secciones de 20 afirmaciones.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">
    <b>Cómo responder:</b> valora cada afirmación según cómo se aplica a ti durante
    la mayor parte de tu vida. Debes contestar las 60 afirmaciones.
    </div>
    """,
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None

with st.form("dosha_form"):
    name = st.text_input("Nombre de la persona (opcional)", placeholder="Ejemplo: Francisco")
    st.caption("El nombre solo se utiliza para identificar el informe descargable.")

    tabs = st.tabs(["🌬️ Vata", "🔥 Pitta", "🌿 Kapha"])
    selected_scores = {dosha: [] for dosha in QUESTIONNAIRES}

    for tab, (dosha, questions) in zip(tabs, QUESTIONNAIRES.items()):
        with tab:
            st.subheader(f"Sección {dosha}")
            st.markdown(
                """
                <div class="scale">
                <b>Escala gradual:</b> la intensidad aumenta de 1 a 6.<br>
                1 = no se aplica en absoluto &nbsp;·&nbsp; 2 = casi no se aplica<br>
                3 = a veces, en menor grado &nbsp;·&nbsp; 4 = a veces, en mayor grado<br>
                5 = generalmente &nbsp;·&nbsp; 6 = casi siempre
                </div>
                """,
                unsafe_allow_html=True,
            )

            for index, question in enumerate(questions, start=1):
                st.markdown(
                    f'<div class="question-number">{index}. {question}</div>',
                    unsafe_allow_html=True,
                )
                choice = st.selectbox(
                    "Puntuación",
                    options=["Selecciona una puntuación"] + list(SCORE_OPTIONS),
                    key=f"{dosha.lower()}_{index}",
                    label_visibility="collapsed",
                )
                selected_scores[dosha].append(SCORE_OPTIONS.get(choice))

    submitted = st.form_submit_button(
        "Calcular mis porcentajes", type="primary", use_container_width=True
    )

if submitted:
    missing_by_dosha = {
        dosha: sum(score is None for score in scores)
        for dosha, scores in selected_scores.items()
    }
    total_missing = sum(missing_by_dosha.values())

    if total_missing:
        details = ", ".join(
            f"{dosha}: {amount}" for dosha, amount in missing_by_dosha.items() if amount
        )
        st.error(
            f"Faltan {total_missing} afirmación(es) por responder ({details}). "
            "Revisa las tres pestañas."
        )
    else:
        section_scores = {
            dosha: sum(scores) for dosha, scores in selected_scores.items()
        }
        grand_total, percentages, ranked, profile, explanation = calculate_result(
            section_scores
        )
        st.session_state.result = {
            "name": name,
            "section_scores": section_scores,
            "grand_total": grand_total,
            "percentages": percentages,
            "ranked": ranked,
            "profile": profile,
            "explanation": explanation,
        }

if st.session_state.result:
    result = st.session_state.result
    st.divider()
    st.header("Resultado de la evaluación")
    st.success(f"Perfil: **{result['profile']}**. {result['explanation']}")

    for dosha in result["ranked"]:
        info = DOSHA_INFO[dosha]
        score = result["section_scores"][dosha]
        percentage = result["percentages"][dosha]
        st.markdown(
            f"""
            <div class="result-card" style="--accent:{info['color']}">
                <h3>{info['emoji']} {dosha}: {percentage:.1f}%</h3>
                <p><b>{score} puntos de 120.</b> Elementos: {info['elements']}.</p>
                <p>Se relaciona con {info['summary']}.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(percentage / 100)

    st.caption(
        f"Suma de los tres resultados: {result['grand_total']} puntos. "
        "Los porcentajes comparativos suman aproximadamente 100%."
    )

    report = build_report(
        result["name"],
        result["section_scores"],
        result["grand_total"],
        result["percentages"],
        result["profile"],
        result["explanation"],
    )
    st.download_button(
        "Descargar resultado en TXT",
        data=report.encode("utf-8"),
        file_name="resultado_doshas.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if st.button("Realizar una nueva evaluación", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.divider()
with st.expander("Información importante"):
    st.write(
        "La puntuación de cada dosha puede variar entre 20 y 120. El porcentaje se "
        "calcula dividiendo el total de cada dosha entre la suma de Vata, Pitta y "
        "Kapha. Esta herramienta tiene fines educativos y no constituye diagnóstico "
        "médico ni recomendación de tratamiento."
    )
