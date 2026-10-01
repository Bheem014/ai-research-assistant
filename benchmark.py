
"""
Ollama Llama 3.2 1B Benchmark
AI Research Assistant

Tests:
- Model availability
- Response latency
- Tokens generated
- Tokens/second
- Basic answer quality
- Error handling
- Overall benchmark summary

Requirements:
    Ollama running locally
    Model: llama3.2:1b

Run:
    python benchmark.py
"""

import json
import time
import statistics
import urllib.request
import urllib.error


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

# Fixed benchmark questions
QUESTIONS = [
    {
        "category": "General Knowledge",
        "question": "What is the difference between RAM and ROM? Explain briefly."
    },
    {
        "category": "Python",
        "question": "Explain the difference between a Python list and tuple with one example."
    },
    {
        "category": "Machine Learning",
        "question": "What is overfitting in machine learning and how can it be reduced?"
    },
    {
        "category": "AI",
        "question": "What is the difference between supervised and unsupervised learning?"
    },
    {
        "category": "Deep Learning",
        "question": "What is a neural network? Explain the role of weights, biases, and activation functions."
    },
    {
        "category": "Computer Science",
        "question": "Explain what an API is and give a simple real-world example."
    },
    {
        "category": "Research",
        "question": "What are the main steps involved in conducting a technical research study?"
    },
    {
        "category": "Reasoning",
        "question": "If a system processes 100 documents in 20 seconds, approximately how many documents can it process in 2 minutes?"
    },
    {
        "category": "Multi-Agent AI",
        "question": "What is a multi-agent AI system? Explain how multiple specialized agents can work together."
    },
    {
        "category": "Technical Analysis",
        "question": "Explain why retrieving multiple sources can improve the reliability of an AI-generated research report."
    },
]


# ============================================================
# OLLAMA REQUEST
# ============================================================

def query_ollama(prompt):
    """
    Send a prompt to Ollama and return:
        response text
        total duration
        evaluation duration
        prompt tokens
        generated tokens
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 300
        }
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        end_time = time.perf_counter()

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Ollama.\n"
            f"Make sure Ollama is running.\n"
            f"Error: {error}"
        )

    except Exception as error:
        raise RuntimeError(f"Ollama request failed: {error}")

    total_time = end_time - start_time

    response_text = result.get("response", "").strip()

    prompt_tokens = result.get("prompt_eval_count", 0)
    generated_tokens = result.get("eval_count", 0)

    prompt_eval_ns = result.get("prompt_eval_duration", 0)
    eval_ns = result.get("eval_duration", 0)

    # Convert nanoseconds to seconds
    prompt_eval_time = prompt_eval_ns / 1_000_000_000
    generation_time = eval_ns / 1_000_000_000

    if generation_time > 0:
        tokens_per_second = generated_tokens / generation_time
    else:
        tokens_per_second = 0

    return {
        "response": response_text,
        "total_time": total_time,
        "prompt_tokens": prompt_tokens,
        "generated_tokens": generated_tokens,
        "generation_time": generation_time,
        "tokens_per_second": tokens_per_second,
        "prompt_eval_time": prompt_eval_time,
    }


# ============================================================
# BASIC QUALITY CHECK
# ============================================================

def evaluate_quality(question, answer):
    """
    Simple heuristic quality evaluation.

    This is NOT a human-level evaluation.
    It checks whether the model produced a meaningful response.
    """

    score = 0

    if len(answer.strip()) > 50:
        score += 2

    if len(answer.strip()) > 150:
        score += 1

    if len(answer.strip()) > 300:
        score += 1

    # Penalize obvious failure responses
    failure_words = [
        "i don't know",
        "i cannot answer",
        "i'm unable",
        "error",
        "cannot help"
    ]

    lower_answer = answer.lower()

    for word in failure_words:
        if word in lower_answer:
            score -= 2

    # Check whether the answer contains useful structure
    if any(symbol in answer for symbol in [".", ":", "-", "\n"]):
        score += 1

    score = max(0, min(score, 5))

    return score


# ============================================================
# PRINT RESULT
# ============================================================

def print_result(index, question_data, result, quality):
    print("\n" + "=" * 75)
    print(f"TEST {index}/{len(QUESTIONS)}")
    print("=" * 75)

    print(f"Category       : {question_data['category']}")
    print(f"Question       : {question_data['question']}")

    print("\n--- MODEL RESPONSE ---")
    print(result["response"])

    print("\n--- PERFORMANCE ---")
    print(f"Total latency  : {result['total_time']:.2f} seconds")
    print(f"Prompt tokens  : {result['prompt_tokens']}")
    print(f"Output tokens  : {result['generated_tokens']}")
    print(f"Generation     : {result['generation_time']:.2f} seconds")
    print(f"Tokens/sec     : {result['tokens_per_second']:.2f}")
    print(f"Quality score  : {quality}/5")


# ============================================================
# MAIN BENCHMARK
# ============================================================

def main():

    print("\n")
    print("=" * 75)
    print("       OLLAMA LLM BENCHMARK")
    print("=" * 75)

    print(f"Model          : {MODEL}")
    print(f"Ollama API     : {OLLAMA_URL}")
    print(f"Questions      : {len(QUESTIONS)}")

    print("\nChecking Ollama connection...")

    try:
        test_result = query_ollama(
            "Reply with exactly one word: READY"
        )

        print("Ollama status  : CONNECTED")
        print(f"Model response : {test_result['response']}")

    except Exception as error:

        print("\nERROR")
        print("-" * 75)
        print(error)

        print("\nTry:")
        print("1. Start Ollama")
        print("2. Run: ollama list")
        print("3. Verify llama3.2:1b exists")
        print("4. Run: ollama run llama3.2:1b")

        return

    # --------------------------------------------------------
    # Run benchmark
    # --------------------------------------------------------

    results = []

    print("\n")
    print("=" * 75)
    print("STARTING BENCHMARK")
    print("=" * 75)

    benchmark_start = time.perf_counter()

    for index, question_data in enumerate(QUESTIONS, start=1):

        prompt = f"""
You are an AI research assistant.

Answer the following question accurately and clearly.

Question:
{question_data['question']}

Requirements:
- Be technically accurate.
- Explain the answer clearly.
- Do not invent facts.
- Keep the answer reasonably concise.
"""

        try:

            result = query_ollama(prompt)

            quality = evaluate_quality(
                question_data["question"],
                result["response"]
            )

            result["category"] = question_data["category"]
            result["quality"] = quality

            results.append(result)

            print_result(
                index,
                question_data,
                result,
                quality
            )

        except Exception as error:

            print("\nERROR during test:")
            print(error)

    benchmark_end = time.perf_counter()

    total_benchmark_time = benchmark_end - benchmark_start

    # --------------------------------------------------------
    # Summary calculations
    # --------------------------------------------------------

    if not results:
        print("\nNo successful benchmark results.")
        return

    latencies = [
        result["total_time"]
        for result in results
    ]

    speeds = [
        result["tokens_per_second"]
        for result in results
        if result["tokens_per_second"] > 0
    ]

    output_tokens = [
        result["generated_tokens"]
        for result in results
    ]

    quality_scores = [
        result["quality"]
        for result in results
    ]

    average_latency = statistics.mean(latencies)

    median_latency = statistics.median(latencies)

    average_speed = (
        statistics.mean(speeds)
        if speeds
        else 0
    )

    average_output_tokens = statistics.mean(
        output_tokens
    )

    average_quality = statistics.mean(
        quality_scores
    )

    total_output_tokens = sum(
        output_tokens
    )

    # --------------------------------------------------------
    # Overall score
    # --------------------------------------------------------

    # This is only a benchmark indicator,
    # not an industry-standard LLM score.

    quality_percentage = (
        average_quality / 5
    ) * 100

    if average_speed >= 20:
        speed_rating = "FAST"
    elif average_speed >= 10:
        speed_rating = "MODERATE"
    elif average_speed > 0:
        speed_rating = "SLOW"
    else:
        speed_rating = "UNKNOWN"

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\n\n")
    print("=" * 75)
    print("                    BENCHMARK SUMMARY")
    print("=" * 75)

    print(f"Model                  : {MODEL}")

    print(
        f"Successful tests       : "
        f"{len(results)}/{len(QUESTIONS)}"
    )

    print(
        f"Total benchmark time   : "
        f"{total_benchmark_time:.2f} seconds"
    )

    print(
        f"Average latency        : "
        f"{average_latency:.2f} seconds"
    )

    print(
        f"Median latency         : "
        f"{median_latency:.2f} seconds"
    )

    print(
        f"Average output tokens  : "
        f"{average_output_tokens:.1f}"
    )

    print(
        f"Total output tokens    : "
        f"{total_output_tokens}"
    )

    print(
        f"Average tokens/sec     : "
        f"{average_speed:.2f}"
    )

    print(
        f"Speed category         : "
        f"{speed_rating}"
    )

    print(
        f"Average quality        : "
        f"{average_quality:.2f}/5"
    )

    print(
        f"Quality percentage     : "
        f"{quality_percentage:.1f}%"
    )

    print("=" * 75)

    print("\nPER-TEST PERFORMANCE")
    print("-" * 75)

    print(
        f"{'Test':<6}"
        f"{'Category':<22}"
        f"{'Latency':<12}"
        f"{'Tok/s':<12}"
        f"{'Quality':<10}"
    )

    print("-" * 75)

    for index, result in enumerate(results, start=1):

        category = result["category"]

        if len(category) > 20:
            category = category[:20]

        print(
            f"{index:<6}"
            f"{category:<22}"
            f"{result['total_time']:<12.2f}"
            f"{result['tokens_per_second']:<12.2f}"
            f"{result['quality']}/5"
        )

    print("-" * 75)

    # --------------------------------------------------------
    # Save JSON results
    # --------------------------------------------------------

    report = {
        "model": MODEL,
        "ollama_url": OLLAMA_URL,
        "questions": len(QUESTIONS),
        "successful_tests": len(results),
        "total_benchmark_time": total_benchmark_time,
        "average_latency": average_latency,
        "median_latency": median_latency,
        "average_output_tokens": average_output_tokens,
        "total_output_tokens": total_output_tokens,
        "average_tokens_per_second": average_speed,
        "average_quality": average_quality,
        "quality_percentage": quality_percentage,
        "speed_category": speed_rating,
        "tests": results,
    }

    output_file = "benchmark_results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nDetailed results saved to:")
    print(output_file)

    print("\nBenchmark completed.")
    print("=" * 75)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()