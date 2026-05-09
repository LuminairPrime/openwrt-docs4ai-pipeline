import re

with open("docs/plans/v13/openwrt-mistake-discovery/process_openwrt_archives.py", "r") as f:
    content = f.read()

# Let's replace the conflict markers with just the HEAD code which is our optimized version
# Find everything between <<<<<<< HEAD and =======
def fix_conflict(text):
    import re
    pattern = re.compile(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> origin/main", re.DOTALL)

    def repl(match):
        head = match.group(1)
        main = match.group(2)
        # Use HEAD because it contains our list comprehension optimization
        return head

    return pattern.sub(repl, text)

new_content = fix_conflict(content)
with open("docs/plans/v13/openwrt-mistake-discovery/process_openwrt_archives.py", "w") as f:
    f.write(new_content)
