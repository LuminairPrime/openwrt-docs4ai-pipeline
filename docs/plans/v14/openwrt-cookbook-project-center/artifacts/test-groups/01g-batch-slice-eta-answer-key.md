# Eta Batch Answer Key

**Batch:** `01g-batch-slice-eta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 18

---

## Scenario 18 — LuCI JS async load/render lifecycle

**PASS criteria:** Must define `rpc.declare()`, fetch live state in `load()`, and build a `form.Map` in `render()` using the resolved data rather than issuing live RPC calls during render.

**Canonical Answer:**

```js
'use strict';
'require form';
'require rpc';
'require uci';
'require view';

const callStatus = rpc.declare({
	object: 'myservice',
	method: 'status',
	expect: { '': {} }
});

return view.extend({
	load() {
		return Promise.all([
			L.resolveDefault(callStatus(), {}),
			L.resolveDefault(uci.load('myservice'), {})
		]);
	},

	render([status]) {
		let m = new form.Map('myservice', _('My Service'));
		let s = m.section(form.NamedSection, 'main', 'settings');
		s.addremove = false;

		let o = s.option(form.DummyValue, '_status', _('Current state'));
		o.rawhtml = true;
		o.cfgvalue = function() {
			return status.running ? _('Running') : _('Stopped');
		};

		return m.render();
	}
});
```

**Pattern Notes:**

- `load()` owns the async fetch boundary
- `render()` consumes resolved data and returns `m.render()`
- raw `fetch()` or live RPC calls in `render()` fail the scenario
