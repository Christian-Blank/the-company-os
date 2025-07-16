RuleDiscoveryService.discover_rules() blindly does:

frontmatter = yaml.safe_load(raw_frontmatter)      # ← whatever PyYAML gives back
rule_doc    = RuleDocument(**frontmatter)          # ← expands the dict into kwargs

When you call a function with the **mapping splat, every key in that mapping must be a plain str.
If even one key is not a string, CPython raises

TypeError: keywords must be strings

That’s exactly what is happening in all three failing edge-case files:

file	What PyYAML returns	Why the key isn’t a str
malformed.rules.md	{'title':'Malformed', …, None: 'broken yaml'}	The line ": broken yaml" is parsed as a mapping whose key is empty → None
no_frontmatter.rules.md	None (because there’s no --- … --- block)	You then try RuleDocument(**None) – PyYAML didn’t give you a dict at all
empty.rules.md	None (empty string)	Same as above

In all cases frontmatter is not a clean dict[str, Any], so the double-asterisk expansion fails.

How to fix it
	1.	Validate the parsed front-matter before unpacking:

try:
    frontmatter = yaml.safe_load(front) or {}
    if not isinstance(frontmatter, dict) or not all(isinstance(k, str) for k in frontmatter):
        raise ValueError("Front-matter must be a mapping with string keys")
    rule_doc = RuleDocument(**frontmatter)
except (yaml.YAMLError, ValueError, TypeError) as exc:
    errors.append(f"{path.name}: {exc}")
    continue        # skip this file

	2.	Treat missing/empty front-matter as “no rule here” instead of an error, if that’s your intended behaviour.
	3.	Add a unit-test case for the “empty key” situation so you don’t regress later.

Once you gate on isinstance(frontmatter, dict) and all(str keys), discover_rules() will collect the expected errors and your three tests should pass.