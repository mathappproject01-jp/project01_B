# birthday_problem_simulator_4.py

import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# ==================================================
# 日本語フォント
# ==================================================

plt.rcParams["font.family"] = "Yu Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ==================================================
# 画面設定
# ==================================================

st.set_page_config(
    page_title="誕生日一致問題シミュレーター",
    layout="wide"
)

st.title("🎂 誕生日一致問題シミュレーター")

st.write("""
クラスの中に

**「誕生日が同じ人が1組以上いる確率」**

をシミュレーションします。

※ うるう年は考えず、1年を365日とします。
""")

# ==================================================
# シミュレーション設定
# ==================================================

st.subheader("⚙️ シミュレーション設定")

col1, col2, col3 = st.columns([3, 3, 1])

with col1:
    class_size = st.slider(
        "クラス人数",
        min_value=2,
        max_value=60,
        value=40,
        step=1
    )

with col2:
    N = st.slider(
        "試行回数",
        min_value=100,
        max_value=100000,
        value=10000,
        step=100
    )

with col3:
    st.write("")
    st.write("")
    run = st.button(
        "実験開始",
        use_container_width=True
    )

st.info(
    f"現在の設定： クラス人数 {class_size} 人　　試行回数 {N:,} 回"
)

# ==================================================
# 予想入力
# ==================================================

st.subheader("📝 あなたの予想")

prediction = st.number_input(
    "誕生日一致確率が50%を超えるのは何人だと思いますか？",
    min_value=2,
    max_value=100,
    value=30,
    step=1
)

st.write(
    f"あなたの予想： {prediction} 人"
)

# ==================================================
# 探究モード
# ==================================================

st.subheader("🔍 探究モード")

c1, c2, c3 = st.columns(3)

with c1:
    show_theory = st.checkbox(
        "理論値を表示",
        value=False
    )

with c2:
    show_formula = st.checkbox(
        "数式を表示",
        value=False
    )

with c3:
    show_graph = st.checkbox(
        "理論グラフを表示",
        value=False
    )

# ==================================================
# 理論値関数
# ==================================================

def theoretical_probability(n):

    p = 1.0

    for i in range(n):
        p *= (365 - i) / 365

    return 1 - p

# ==================================================
# シミュレーション関数
# ==================================================

def birthday_experiment(class_size):

    birthdays = [
        random.randint(1, 365)
        for _ in range(class_size)
    ]

    return len(set(birthdays)) < class_size

# ==================================================
# 現在人数の理論値
# ==================================================

theory_prob = theoretical_probability(class_size)

# ==================================================
# 理論値表示
# ==================================================

if show_theory:

    st.subheader("理論値")

    st.metric(
        "誕生日が一致する確率",
        f"{theory_prob:.4f}"
    )

# ==================================================
# 数式表示
# ==================================================

if show_formula:

    st.subheader("理論式")

    st.latex(
        r"""
P(\text{一致あり})
=
1-
\prod_{k=0}^{n-1}
\frac{365-k}{365}
"""
    )

    st.write("""
まず「全員の誕生日が異なる確率」を求め、
その余事象として
「少なくとも1組一致する確率」を求めます。
""")

# ==================================================
# シミュレーション
# ==================================================

if run:

    success = 0

    history = []

    for i in range(1, N + 1):

        if birthday_experiment(class_size):
            success += 1

        history.append(success / i)

    sim_prob = success / N

    # ==============================================
    # シミュレーション結果
    # ==============================================

    st.subheader("シミュレーション結果")

    if show_theory:

        colA, colB = st.columns(2)

        with colA:
            st.metric(
                "シミュレーション値",
                f"{sim_prob:.4f}"
            )

        with colB:
            st.metric(
                "理論値",
                f"{theory_prob:.4f}"
            )

    else:

        st.metric(
            "シミュレーション値",
            f"{sim_prob:.4f}"
        )

        st.info(
            "まずはシミュレーション結果だけを見て考察してみましょう。"
        )

    st.info(
        """
一致した実験回数 ÷ 試行回数

で計算しています。

試行回数を増やすほど
結果は安定していきます。
"""
    )

    # ==============================================
    # 理論値との比較
    # ==============================================

    if show_theory:

        st.subheader("理論値との比較")

        result_df = pd.DataFrame({
            "人数": [class_size],
            "シミュレーション値": [sim_prob],
            "理論値": [theory_prob]
        })

        st.dataframe(
            result_df,
            use_container_width=True
        )

    # ==============================================
    # 収束グラフ
    # ==============================================

    st.subheader("試行回数による変化")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        history,
        linewidth=2,
        label="シミュレーション値"
    )

    if show_theory:

        ax.axhline(
            theory_prob,
            color="red",
            linestyle="--",
            linewidth=2,
            label="理論値"
        )

        ax.legend()

    ax.set_xlabel("試行回数")
    ax.set_ylabel("一致確率")
    ax.grid(True)

    st.pyplot(fig)

    # ==============================================
    # 結果の解釈
    # ==============================================

    st.subheader("結果の解釈")

    st.write(
        f"{class_size} 人のクラスで、"
        f"同じ誕生日の人がいる確率は "
        f"{sim_prob:.2%} です。"
    )

    if sim_prob >= 0.5:

        st.success(
            "50%以上の確率で誕生日が一致します。"
        )

    else:

        st.info(
            "まだ50%未満です。"
        )

# ==================================================
# 理論グラフ
# ==================================================

if show_graph:

    st.subheader("人数と誕生日一致確率")

    people = list(range(2, 61))

    probs = [
        theoretical_probability(p)
        for p in people
    ]

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    ax2.plot(
        people,
        probs,
        linewidth=3,
        label="理論値"
    )

    ax2.scatter(
        [class_size],
        [theory_prob],
        color="red",
        s=120
    )

    ax2.axhline(
        0.5,
        linestyle="--",
        color="gray"
    )

    ax2.set_xlabel("人数")
    ax2.set_ylabel("一致確率")

    ax2.set_title(
        "人数と誕生日一致確率"
    )

    ax2.grid(True)

    ax2.legend()

    st.pyplot(fig2)

    # ==========================================
    # 50%を超える人数
    # ==========================================

    boundary = None

    for n in range(2, 100):

        if theoretical_probability(n) >= 0.5:

            boundary = n
            break

    st.success(
        f"誕生日一致確率が50%を超える最小人数は {boundary} 人です。"
    )

    # ==========================================
    # 予想との比較
    # ==========================================

    diff = prediction - boundary

    compare_df = pd.DataFrame({
        "項目": [
            "あなたの予想",
            "実際の人数",
            "差"
        ],
        "値": [
            prediction,
            boundary,
            diff
        ]
    })

    st.dataframe(
        compare_df,
        use_container_width=True
    )

    if diff == 0:

        st.balloons()

        st.success(
            "🎉 予想がぴったり一致しました！"
        )

    elif diff > 0:

        st.info(
            f"予想は {prediction} 人でした。"
            f" 実際より {diff} 人多く見積もっていました。"
        )

    else:

        st.info(
            f"予想は {prediction} 人でした。"
            f" 実際より {-diff} 人少なく見積もっていました。"
        )

# ==================================================
# 考察
# ==================================================

st.subheader("📝 考察のヒント")

st.write("""
① 何人で50％を超えると予想しましたか。

② 予想と実際にはどのくらい差がありましたか。

③ なぜ23人程度で50％を超えるのでしょうか。

④ 人数が増えると一致確率はどのように変化しますか。

⑤ シミュレーション値は理論値に近づいていますか。

⑥ 40人学級では一致確率はどのくらいになりますか。

⑦ 人数をさらに増やすと確率はどうなるでしょうか。

⑧ 「365日あるのだから180人くらい必要」と感じた人は、
なぜそう考えたのでしょうか。

⑨ 比較する組の数
nC2
との関係を考えてみましょう。
""")
