# Methodology sync

This repository is the English full edition of one method. [agent-system-design-cn](https://github.com/geniusjia666/agent-system-design-cn) is the Chinese full edition of the same methodology. They are language editions, not unrelated products.

[VERSION](VERSION) is the shared methodology version. Both editions start at **0.1.0**. That number is not a GitHub Release, and this repository does not create a tag or a release for it.

## Source edition

The English source edition is the skill under [skills/agent-system-design](skills/agent-system-design/SKILL.md). Those files were imported byte for byte from the English archive. [PROVENANCE.md](PROVENANCE.md) records that import. The Chinese source edition is maintained in the sibling repository. This repository does not vendor it.

## Same numbered version

A methodology change uses one new number in both repositories. While the editions still describe the same method, both `VERSION` files stay on the same number, currently 0.1.0. This repository cannot write the sibling's `VERSION` file.

## When to update both

Update both editions, and set both to the same new version number, when the method changes in either language. That includes the 7-step process, the four architecture tiers, the 21 patterns, the 21 review dimensions, the handoff contract, or any other guidance that would make the editions describe different methods.

An edition-local fix that does not change the method can stay on the current number. Examples are a spelling fix, a broken link, or install-note wording in one language. If that fix changes meaning, treat it as a methodology change and update both editions.

## No automated sync

There is no automated sync. Nothing in this repository copies, watches, mirrors, or deploys the sibling repository. Changing this edition does not change the other one. A person has to open the matching change in [agent-system-design-cn](https://github.com/geniusjia666/agent-system-design-cn) and set both `VERSION` files to the same number.
