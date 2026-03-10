import datetime

def compute_stats(numbers):
  if not numbers:
    return None
  total = sum(numbers)
  count = len(numbers)
  avg = total / count
  return {
    "min": min(numbers),
    "max": max(numbers),
    "sum": total,
    "count": count,
    "avg": avg,
  }

def main():
  print("Simple Python stats demo")
  print("Enter integers separated by spaces:")
  raw = input("> ").strip()
  if not raw:
    print("No data provided.")
    return

  nums = []
  for part in raw.split():
    try:
      nums.append(int(part))
    except ValueError:
      print(f"Skipping invalid value: {part!r}")

  stats = compute_stats(nums)
  if not stats:
    print("No valid numbers to process.")
    return

  now = datetime.datetime.now().isoformat(timespec="seconds")
  print(f"\nResults at {now}")
  for key, value in stats.items():
    print(f"{key}: {value}")

if __name__ == "__main__":
  main()
