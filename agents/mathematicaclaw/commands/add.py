def run(args):
    """Add numbers"""
    try:
        nums = [float(x) for x in args.split()]
        return f"Sum: {sum(nums)}"
    except:
        return "Usage: add 2 3 4"
