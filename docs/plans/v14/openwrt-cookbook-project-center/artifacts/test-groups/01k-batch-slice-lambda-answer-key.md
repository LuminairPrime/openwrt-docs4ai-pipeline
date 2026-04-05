# Lambda Batch Answer Key

**Batch:** `01k-batch-slice-lambda.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 22

---

## Scenario 22 — C blobmsg parse plus nested reply

**PASS criteria:** Must define a `blobmsg_policy` array, parse input with `blobmsg_parse()`, and reply using `struct blob_buf`, `blobmsg_open_table()`, and `ubus_send_reply()`.

**Canonical Answer:**

```c
enum {
	REQ_ADDR,
	__REQ_MAX,
};

static const struct blobmsg_policy req_policy[__REQ_MAX] = {
	[REQ_ADDR] = { .name = "addr", .type = BLOBMSG_TYPE_STRING },
};

static int my_handler(struct ubus_context *ctx, struct ubus_object *obj,
	struct ubus_request_data *req, const char *method, struct blob_attr *msg)
{
	struct blob_attr *tb[__REQ_MAX];
	struct blob_buf b = {};
	void *result;

	blobmsg_parse(req_policy, __REQ_MAX, tb, blob_data(msg), blob_len(msg));
	if (!tb[REQ_ADDR])
		return UBUS_STATUS_INVALID_ARGUMENT;

	blob_buf_init(&b, 0);
	result = blobmsg_open_table(&b, "result");
	blobmsg_add_u8(&b, "accepted", true);
	blobmsg_add_string(&b, "addr", blobmsg_get_string(tb[REQ_ADDR]));
	blobmsg_close_table(&b, result);

	ubus_send_reply(ctx, req, b.head);
	blob_buf_free(&b);
	return 0;
}
```

**Pattern Notes:**

- raw casts or string-built JSON fail the scenario
- this is the combined parse-plus-reply contract, not only one side of it
