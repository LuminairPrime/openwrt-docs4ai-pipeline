---
module: luci-examples
total_token_count: 2139
section_count: 3
is_monolithic: false
is_sharded_part: true
part_number: 2
part_count: 2
generated: '2026-08-01T13:35:11.474886+00:00'
---

# luci-examples Bundled Reference (Part 2 of 2)

> **Contains:** 3 documents
> **Tokens:** ~2139 (cl100k_base)
> **Index:** [./bundled-reference.md](./bundled-reference.md)

---

# rpc-jsonmap-tablesection.js
```javascript
'use strict';
'require form';
'require rpc';
'require view';

/*
Declare the RPC calls that are needed. The object value maps to the name
listed by the shell command

$ ubus list

Custom ucode scripts can be placed in /usr/share/rpcd/ucode, and must emit JSON.

Permissions to make these calls must be granted in /usr/share/rpcd/acl.d
via a file named the same as the application package name (luci-app-example)
*/
const load_sample2 = rpc.declare({
	object: 'luci.example',
	method: 'get_sample2'
});

function capitalize(message) {
	var arr = message.split(" ");
	for (var i = 0; i < arr.length; i++) {
		arr[i] = arr[i].charAt(0).toUpperCase() + arr[i].slice(1);
	}
	return arr.join(" ");
}

return view.extend({
	generic_failure: function (message) {
		// Map an error message into a div for rendering
		return E('div', {
			'class': 'error'
		}, [_('RPC call failure: '), message])
	},
	render_sample2_using_jsonmap: function (sample) {
		console.log('render_sample2_using_jsonmap()');
		console.log(sample);

		// Handle errors as before
		if (sample.error) {
			return this.generic_failure(sample.error)
		}

		// Variables you'll usually see declared in LuCI JS apps; forM, Section, Option
		let m, s, o;

		/*
		LuCI has the concept of a JSONMap. This will map a structured object to
		a configuration form. Normally you'd use this with a UCI-powered result,
		since saving via an RPC call is going to be more difficult than using the
		built-in UCI/ubus libraries.
        
		https://openwrt.github.io/luci/jsapi/LuCI.form.JSONMap.html
        
		Execute   ubus call luci.example get_sample2   to see the JSON being used.
		*/
		m = new form.JSONMap(sample, _('JSONMap TableSection Sample'), _(
			'See browser console for raw data'));
		// Make the form read-only; this only matters if the apply/save/reset handlers
		// are not replaced with null to disable them.
		m.readonly = true;
		// Set up for a tabbed display
		m.tabbed = false;

		const option_names = Object.keys(sample);
		for (var i = option_names.length - 1; i >= 0; i--) {
			var option_name = option_names[i];
			var display_name = option_name.replace("_", " ");
			s = m.section(form.TableSection, option_name, capitalize(display_name), _(
				'Description for this table section'))
			o = s.option(form.Value, 'name', _('Option name'));
			o = s.option(form.Value, 'value', _('Option value'));
			o = s.option(form.DynamicList, 'parakeets', 'Parakeets');
		}
		return m;
	},
	/*
	load() is called on first page load, and the results of each promise are
	placed in an array in the call order. This array is passed to the render()
	function as the first argument.
	*/
	load: function () {
		return Promise.all([
			load_sample2(),
		]);
	},
	// render() is called by the LuCI framework to do any data manipulation, and the
	// return is used to modify the DOM that the browser shows.
	render: function (data) {
		// data[0] will be the result from load_sample2
		var sample2 = data[0] || {};
		return this.render_sample2_using_jsonmap(sample2).render();
	},
	/*
	Since this is a view-only screen, the handlers are disabled
	Normally, when using something like Map or JSONMap, you would 
	not null out these handlers, so that the form can be saved/applied.
    
	With a RPC data source, you would need to define custom handlers
	that verify the changes, and make RPC calls to a backend that can
	process the request.
	*/
	handleSave: null,
	handleSaveApply: null,
	handleReset: null
})
```

---

# rpc-jsonmap-typedsection.js
```javascript
'use strict';
'require form';
'require rpc';
'require view';

/*
Declare the RPC calls that are needed. The object value maps to the name
listed by the shell command

$ ubus list

Custom ucode scripts can be placed in /usr/share/rpcd/ucode, and must emit JSON.

Permissions to make these calls must be granted in /usr/share/rpcd/acl.d
via a file named the same as the application package name (luci-app-example)
*/
const load_sample2 = rpc.declare({
	object: 'luci.example',
	method: 'get_sample2'
});

function capitalize(message) {
	var arr = message.split(" ");
	for (var i = 0; i < arr.length; i++) {
		arr[i] = arr[i].charAt(0).toUpperCase() + arr[i].slice(1);
	}
	return arr.join(" ");
}

return view.extend({
	generic_failure: function (message) {
		// Map an error message into a div for rendering
		return E('div', {
			'class': 'error'
		}, [_('RPC call failure: '), message])
	},
	render_sample2_using_jsonmap: function (sample) {
		console.log('render_sample2_using_jsonmap()');
		console.log(sample);

		// Handle errors as before
		if (sample.error) {
			return this.generic_failure(sample.error)
		}

		// Variables you'll usually see declared in LuCI JS apps; forM, Section, Option
		let m, s, o;

		/*
		LuCI has the concept of a JSONMap. This will map a structured object to
		a configuration form. Normally you'd use this with a UCI-powered result,
		since saving via an RPC call is going to be more difficult than using the
		built-in UCI/ubus libraries.
        
		https://openwrt.github.io/luci/jsapi/LuCI.form.JSONMap.html
        
		Execute   ubus call luci.example get_sample2   to see the JSON being used.
		*/
		m = new form.JSONMap(sample, _('JSONMap TypedSection Sample'), _(
			'See browser console for raw data'));
		// Make the form read-only; this only matters if the apply/save/reset handlers
		// are not replaced with null to disable them.
		m.readonly = true;
		// Set up for a tabbed display
		m.tabbed = true;

		const option_names = Object.keys(sample);
		for (var i = option_names.length - 1; i >= 0; i--) {
			var option_name = option_names[i];
			var display_name = option_name.replace("_", " ");
			s = m.section(form.TypedSection, option_name, capitalize(display_name), _(
				'Description for this typed section'))
			o = s.option(form.Value, 'name', _('Option name'));
			o = s.option(form.Value, 'value', _('Option value'));
			o = s.option(form.DynamicList, 'parakeets', 'Parakeets');
		}
		return m;
	},
	/*
	load() is called on first page load, and the results of each promise are
	placed in an array in the call order. This array is passed to the render()
	function as the first argument.
	*/
	load: function () {
		return Promise.all([
			load_sample2(),
		]);
	},
	// render() is called by the LuCI framework to do any data manipulation, and the
	// return is used to modify the DOM that the browser shows.
	render: function (data) {
		// data[0] will be the result from load_sample2
		var sample2 = data[0] || {};
		return this.render_sample2_using_jsonmap(sample2).render();
	},
	/*
	Since this is a view-only screen, the handlers are disabled
	Normally, when using something like Map or JSONMap, you would 
	not null out these handlers, so that the form can be saved/applied.
    
	With a RPC data source, you would need to define custom handlers
	that verify the changes, and make RPC calls to a backend that can
	process the request.
	*/
	handleSave: null,
	handleSaveApply: null,
	handleReset: null
})
```

---

# example.uc
```ucode
#!/usr/bin/env ucode

'use strict';

import { cursor } from 'uci';

// Rather than parse files in /etc/config, we can use `cursor`.
const uci = cursor();

const methods = {
	get_sample1: {
		call: function() {
			const num_cats = uci.get('example', 'animals', 'num_cats');
			const num_dogs = uci.get('example', 'animals', 'num_dogs');
			const num_parakeets = uci.get('example', 'animals', 'num_parakeets');
			const result = {
				num_cats,
				num_dogs,
				num_parakeets,
				is_this_real: false,
				not_found: null,
			};

			uci.unload();
			return result;
		}
	},

	get_sample2: {
		call: function() {
			const result = {
				option_one: {
					name: "Some string value",
					value: "A value string",
					parakeets: ["one", "two", "three"],
				},
				option_two: {
					name: "Another string value",
					value: "And another value",
					parakeets: [3, 4, 5],
				},
			};
			return result;
		}
	}
};

return { 'luci.example': methods };

```
