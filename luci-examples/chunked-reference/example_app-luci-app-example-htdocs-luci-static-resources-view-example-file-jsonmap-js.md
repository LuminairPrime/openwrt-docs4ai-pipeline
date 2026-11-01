---
title: file-jsonmap.js
module: luci-examples
origin_type: example_app
token_count: 832
source_file: L1-raw/luci-examples/example_app-luci-app-example-htdocs-luci-static-resources-view-example-file-jsonmap-js.md
last_pipeline_run: '2026-11-01T18:17:43.472245+00:00'
source_commit: unknown
source_url: https://github.com/openwrt/luci/blob/unknown/applications/luci-app-example/htdocs/luci-static/resources/view/example/file-jsonmap.js
source_locator: applications/luci-app-example/htdocs/luci-static/resources/view/example/file-jsonmap.js
language: javascript
---

> **Source:** [https://github.com/openwrt/luci/blob/unknown/applications/luci-app-example/htdocs/luci-static/resources/view/example/file-jsonmap.js](https://github.com/openwrt/luci/blob/unknown/applications/luci-app-example/htdocs/luci-static/resources/view/example/file-jsonmap.js)
> **Kind:** example_app | **Commit:** unknown | **Method:** normalized
> **Normalized:** 2026-11-01

# file-jsonmap.js
```javascript
'use strict';
'require form';
'require fs';
'require view';

/*
A JSONMap backed by a JSON file, with saving.

form.JSONMap keeps its data in memory: its save() does nothing, and the
form stores every value as a string. To persist changes, handleSave() calls
map.save() with a callback. The callback runs after the form has been parsed
and validated, reads the sections back from map.data, converts values to the
types the file should hold, and writes the file with fs.write().

Reading and writing the file must be granted in the "file" scope of
/usr/share/rpcd/acl.d/luci-app-example.json. The UCI defaults script
(80_example) creates /etc/example.json on install.
*/
const FILE = '/etc/example.json';

return view.extend({
	load: function () {
		return L.resolveDefault(fs.read(FILE), '{}');
	},

	render: function (content) {
		let data, m, s, o;

		try {
			data = JSON.parse(content);
		}
		catch (e) {
			data = {};
		}

		/*
		JSONMap takes { section_type: object or array of objects }. An object
		becomes a named section; each array entry becomes an anonymous section
		of that type, which is what lets a TypedSection add and remove them.
		*/
		m = new form.JSONMap({
			animals: L.isObject(data.animals) ? data.animals : {},
			pet: Array.isArray(data.pets) ? data.pets : []
		}, _('File JSONMap Sample'), _('Edits %s; changes are written back on Save.').format(FILE));

		s = m.section(form.NamedSection, 'animals', 'animals', _('Animals'));
		o = s.option(form.Value, 'num_cats', _('Number of cats'));
		o.datatype = 'uinteger';
		o = s.option(form.Value, 'num_dogs', _('Number of dogs'));
		o.datatype = 'uinteger';

		s = m.section(form.TypedSection, 'pet', _('Pets'));
		s.anonymous = true;
		s.addremove = true;
		o = s.option(form.Value, 'name', _('Name'));
		o.rmempty = false;
		o = s.option(form.ListValue, 'species', _('Species'));
		o.value('cat', _('Cat'));
		o.value('dog', _('Dog'));
		o.value('parakeet', _('Parakeet'));

		this.map = m;
		this.file = data;
		return m.render();
	},

	handleSave: function (ev) {
		const m = this.map;
		const file = this.file;

		return m.save(function () {
			// Sections are the objects loaded from the file, unknown keys included;
			// keep everything except the '.name'-style bookkeeping JSONMap adds.
			const fields = (s) => Object.fromEntries(Object.entries(s).filter(([ k ]) => k.charAt(0) != '.'));

			// Start from the file as loaded, so keys the form does not edit survive.
			const out = Object.assign({}, file);
			const animals = fields(m.data.get('json', 'animals') || {});

			// Values come back as strings; restore numbers, drop emptied fields.
			for (const key of [ 'num_cats', 'num_dogs' ]) {
				if (animals[key] != null && animals[key] !== '')
					animals[key] = parseInt(animals[key], 10);
				else
					delete animals[key];
			}

			out.animals = animals;
			out.pets = m.data.sections('json', 'pet').map(fields);

			return fs.write(FILE, JSON.stringify(out, null, '\t') + '\n');
		});
	},

	// There is nothing to apply; the file is the whole state.
	handleSaveApply: null
});

```
