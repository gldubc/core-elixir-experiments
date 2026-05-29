# Type Warning Blocks: no-dynamic cached-deps run

Source log: `results/type-warning-no-dynamic-cached-deps-20260527.log`.

Total extracted type warnings: 145

## AbsintheFederation (1)

### AbsintheFederation #1: └─ lib/absinthe/federation/schema.ex:73:24: Absinthe.Federation.Schema.remove_federated_types_pipeline/1

- Message: incompatible types given to Absinthe.Schema.apply_modifiers/2:

```text
    warning: incompatible types given to Absinthe.Schema.apply_modifiers/2:

        Absinthe.Schema.apply_modifiers(
          Absinthe.Pipeline.upto(
            Absinthe.Pipeline.for_schema(schema,
              prototype_schema: schema.__absinthe_prototype_schema__()
            ),
            {Absinthe.Phase.Schema.Validation.Result, pass: :final}
          ),
          schema
        )

    given types:

        dynamic(), -dynamic(atom())-

    but expected one of:

        term(), %{..., __absinthe_pipeline_modifiers__: term()}

    where "schema" was given the type:

        # type: dynamic(atom())
        # from: lib/absinthe/federation/schema.ex:71:62
        schema.__absinthe_prototype_schema__()

    type warning found at:
    │
 73 │     |> Absinthe.Schema.apply_modifiers(schema)
    │                        ~
    │
    └─ lib/absinthe/federation/schema.ex:73:24: Absinthe.Federation.Schema.remove_federated_types_pipeline/1
```

## Ash (45)

### Ash #1: └─ lib/ash.ex:2279:14: Ash.page/2

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(
            Map.get(
              :lists.last(results),
              :__metadata__
            ),
            :keyset
          )

      given types:

          dynamic() or nil, :keyset

      but expected one of:

          map(), term()

      where "results" was given the type:

          # type: dynamic(not empty_list())
          # from: lib/ash.ex:2274:12
          %Ash.Page.Keyset{results: results, rerun: {query, opts}}

      type warning found at:
      │
 2279 │       |> Map.get(:keyset)
      │              ~
      │
      └─ lib/ash.ex:2279:14: Ash.page/2
```

### Ash #2: └─ lib/ash.ex:2297:14: Ash.page/2

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(
            Map.get(
              List.first(results),
              :__metadata__
            ),
            :keyset
          )

      given types:

          dynamic() or nil, :keyset

      but expected one of:

          map(), term()

      where "results" was given the type:

          # type: dynamic(empty_list() or non_empty_list(term(), term()))
          # from: lib/ash.ex:2295:15
          List.first(results)

      type warning found at:
      │
 2297 │       |> Map.get(:keyset)
      │              ~
      │
      └─ lib/ash.ex:2297:14: Ash.page/2
```

### Ash #3: └─ lib/ash/actions/update/bulk.ex:1929:84: Ash.Actions.Update.Bulk.handle_batch/12

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(Map.get(changeset.context, context_key), :index)

      given types:

          dynamic() or nil, :index

      but expected one of:

          map(), term()

      where "changeset" was given the type:

          # type: dynamic(%{..., context: map()})
          # from: lib/ash/actions/update/bulk.ex:1929:60
          Map.get(changeset.context, context_key)

      where "context_key" was given the type:

          # type: dynamic()
          # from: lib/ash/actions/update/bulk.ex:1872:10
          context_key

      type warning found at:
      │
 1929 │                   metadata_key => changeset.context |> Map.get(context_key) |> Map.get(:index),
      │                                                                                    ~
      │
      └─ lib/ash/actions/update/bulk.ex:1929:84: Ash.Actions.Update.Bulk.handle_batch/12
```

### Ash #4: └─ lib/ash/actions/read/read.ex:1195: Ash.Actions.Read.data_layer_query/5

- Message: the following clause will never match:

```text
      warning: the following clause will never match:

          {:ok, query} ->

      it is expected to match on type:

          dynamic(
            ({...} and not {:ok, term()}) or
              ({:error, %{..., __struct__: atom()} or %{..., __struct__: term(), vars: term()}} and
                 not {:ok, term()}) or ({:error or :ok, term()} and not {:ok, term()}) or atom() or
              bitstring() or empty_list() or float() or fun() or integer() or map() or
              non_empty_list(term(), term()) or pid() or port() or reference() or {:error, binary()}
          )

      type warning found at:
      │
 1195 │           {:ok, query} ->
      │           ~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/read/read.ex:1195: Ash.Actions.Read.data_layer_query/5
```

### Ash #5: └─ lib/ash/actions/update/bulk.ex:1939:84: Ash.Actions.Update.Bulk.handle_batch/12

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(Map.get(changeset.context, context_key), :index)

      given types:

          dynamic() or nil, :index

      but expected one of:

          map(), term()

      where "changeset" was given the types:

          # type: dynamic(not %{..., errors: term(), valid?: false})
          # from: lib/ash/actions/update/bulk.ex:1914:35
          Ash.Actions.Update.run(
            domain,
            changeset,
            action,
            Keyword.merge(opts, atomic_upgrade?: false, return_destroyed?: opts[:return_records?])
          )

          # type: dynamic(%{..., context: map()} and not %{..., errors: term(), valid?: false})
          # from: lib/ash/actions/update/bulk.ex:1939:60
          Map.get(changeset.context, context_key)

      where "context_key" was given the type:

          # type: dynamic()
          # from: lib/ash/actions/update/bulk.ex:1872:10
          context_key

      type warning found at:
      │
 1939 │                   metadata_key => changeset.context |> Map.get(context_key) |> Map.get(:index),
      │                                                                                    ~
      │
      └─ lib/ash/actions/update/bulk.ex:1939:84: Ash.Actions.Update.Bulk.handle_batch/12
```

### Ash #6: └─ lib/ash/actions/destroy/bulk.ex:64: Ash.Actions.Destroy.Bulk.run/6

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        is_atom(action)

    will always evaluate to:

        false

    where "action" was given the type:

        # type: dynamic(not %{..., soft?: true} and not atom())
        # from: lib/ash/actions/destroy/bulk.ex:63:41
        action

    type warning found at:
    │
 64 │     action_name = if is_atom(action), do: action, else: action.name
    │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/ash/actions/destroy/bulk.ex:64: Ash.Actions.Destroy.Bulk.run/6
```

### Ash #7: └─ lib/ash/actions/destroy/bulk.ex:476: Ash.Actions.Destroy.Bulk.run/6

- Message: the following clause will never match:

```text
     warning: the following clause will never match:

         nil ->

     because it attempts to match on the result of:

         action

     which has type:

         dynamic(not %{..., soft?: true} and not atom())

     type warning found at:
     │
 476 │         nil ->
     │         ~~~~~~
     │
     └─ lib/ash/actions/destroy/bulk.ex:476: Ash.Actions.Destroy.Bulk.run/6
```

### Ash #8: └─ lib/ash/actions/update/bulk.ex:2266: Ash.Actions.Update.Bulk.map_batches/5

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          max_concurrency

      will always evaluate to:

          dynamic(not false and not nil)

      where "max_concurrency" was given the type:

          # type: dynamic(not false and not nil)
          # from: lib/ash/actions/update/bulk.ex:2259:21
          max_concurrency =
            if max_concurrency && max_concurrency > 1 && Ash.DataLayer.can?(:async_engine, resource) do
              max_concurrency
            else
              0
            end

      type warning found at:
      │
 2266 │     if max_concurrency && max_concurrency > 1 do
      │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/update/bulk.ex:2266: Ash.Actions.Update.Bulk.map_batches/5
```

### Ash #9: └─ lib/ash/actions/read/read.ex:2806: Ash.Actions.Read.strip_load?/1

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          !Ash.Actions.Helpers.keep_read_action_loads_when_loading?()

      will always evaluate to true because its inner expression has type:

          dynamic(false)

      type warning found at:
      │
 2806 │     initial_data && !Ash.Actions.Helpers.keep_read_action_loads_when_loading?()
      │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/read/read.ex:2806: Ash.Actions.Read.strip_load?/1
```

### Ash #10: └─ lib/ash/actions/destroy/bulk.ex:1887: Ash.Actions.Destroy.Bulk.map_batches/5

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          max_concurrency

      will always evaluate to:

          dynamic(not false and not nil)

      where "max_concurrency" was given the type:

          # type: dynamic(not false and not nil)
          # from: lib/ash/actions/destroy/bulk.ex:1880:21
          max_concurrency =
            if max_concurrency && max_concurrency > 1 && Ash.DataLayer.can?(:async_engine, resource) do
              max_concurrency
            else
              0
            end

      type warning found at:
      │
 1887 │     if max_concurrency && max_concurrency > 1 do
      │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/destroy/bulk.ex:1887: Ash.Actions.Destroy.Bulk.map_batches/5
```

### Ash #11: └─ lib/ash/actions/destroy/bulk.ex:479:9: Ash.Actions.Destroy.Bulk.run/6

- Message: the following clause will never match:

```text
     warning: the following clause will never match:

         name when is_atom(name) ->

     because it attempts to match on the result of:

         action

     which has type:

         dynamic(not %{..., soft?: true} and not atom())

     where "name" was given the type:

         # type: atom()
         # from: lib/ash/actions/destroy/bulk.ex:479:19
         is_atom(name)

     type warning found at:
     │
 479 │         name when is_atom(name) ->
     │         ~
     │
     └─ lib/ash/actions/destroy/bulk.ex:479:9: Ash.Actions.Destroy.Bulk.run/6
```

### Ash #12: └─ lib/ash/actions/read/read.ex:2812: Ash.Actions.Read.prefer_existing_loads?/1

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          !Ash.Actions.Helpers.keep_read_action_loads_when_loading?()

      will always evaluate to true because its inner expression has type:

          dynamic(false)

      type warning found at:
      │
 2812 │       !Ash.Actions.Helpers.keep_read_action_loads_when_loading?()
      │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/read/read.ex:2812: Ash.Actions.Read.prefer_existing_loads?/1
```

### Ash #13: └─ lib/ash/policy/authorizer/authorizer.ex:1444: Ash.Policy.Authorizer.strict_filters/2

- Message: comparison between distinct types found:

```text
      warning: comparison between distinct types found:

          result == nil

      given types:

          dynamic(not nil) == nil

      where "result" was given the type:

          # type: dynamic(not nil)
          # from: lib/ash/policy/authorizer/authorizer.ex:1425:20
          result =
            try do
              ...
            end

      While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

      type warning found at:
      │
 1444 │             if is_nil(result) do
      │             ~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/policy/authorizer/authorizer.ex:1444: Ash.Policy.Authorizer.strict_filters/2
```

### Ash #14: └─ lib/ash/policy/authorizer/authorizer.ex:1484: Ash.Policy.Authorizer.strict_filters/2

- Message: comparison between distinct types found:

```text
      warning: comparison between distinct types found:

          result == nil

      given types:

          dynamic(
            (atom() and not nil) or bitstring() or empty_list() or float() or fun() or integer() or map() or
              non_empty_list(term(), term()) or pid() or port() or reference() or {...}
          ) == nil

      where "result" was given the type:

          # type: dynamic(
            (atom() and not nil) or bitstring() or empty_list() or float() or fun() or integer() or map() or
              non_empty_list(term(), term()) or pid() or port() or reference() or {...}
          )
          # from: lib/ash/policy/authorizer/authorizer.ex:1451:20
          result =
            try do
              ...
            end

      While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

      type warning found at:
      │
 1484 │             if is_nil(result) do
      │             ~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/policy/authorizer/authorizer.ex:1484: Ash.Policy.Authorizer.strict_filters/2
```

### Ash #15: └─ lib/ash/filter/filter.ex:2729:7: Ash.Filter.do_list_refs/5

- Message: the following clause will never match:

```text
      warning: the following clause will never match:

          value when is_list(value) ->

      because it attempts to match on the result of:

          expression

      which has type:

          dynamic(
            not %Ash.Filter{} and not empty_list() and not non_empty_list(term(), term()) and
              not {atom(), term()}
          )

      where "value" was given the type:

          # type: empty_list() or non_empty_list(term(), term())
          # from: lib/ash/filter/filter.ex:2729:18
          is_list(value)

      type warning found at:
      │
 2729 │       value when is_list(value) ->
      │       ~
      │
      └─ lib/ash/filter/filter.ex:2729:7: Ash.Filter.do_list_refs/5
```

### Ash #16: └─ lib/ash/actions/read/read.ex:2222:30: Ash.Actions.Read.load_through_attributes/7

- Message: expected a map or struct when accessing .load in expression:

```text
      warning: expected a map or struct when accessing .load in expression:

          calculation.load

      where "calculation" was given the type:

          # type: dynamic() or nil
          # from: lib/ash/actions/read/read.ex:2219:23
          calculation = Map.get(query.calculations, name)

      hint: "var.field" (without parentheses) means "var" is a map() while "var.fun()" (with parentheses) means "var" is an atom()

      type warning found at:
      │
 2222 │             case calculation.load do
      │                              ~
      │
      └─ lib/ash/actions/read/read.ex:2222:30: Ash.Actions.Read.load_through_attributes/7
```

### Ash #17: └─ lib/ash/data_layer/ets/ets.ex:2243:39: Ash.DataLayer.Ets.log_destroy_query/2

- Message: comparison between distinct types found:

```text
      warning: comparison between distinct types found:

          query.filter != nil

      given types:

          dynamic(not false and not nil) != nil

      where "query" was given the types:

          # type: dynamic(%{..., limit: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2222:16
          query.limit

          # type: dynamic(%{..., limit: term(), offset: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2229:16
          query.offset

          # type: dynamic(%{..., limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2236:16
          query.sort

          # type: dynamic(%{..., filter: term(), limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2243:16
          query.filter

          # type: dynamic(%{..., filter: not false and not nil, limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2243:16
          query.filter

      While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

      type warning found at:
      │
 2243 │       if query.filter && query.filter != nil && query.filter.expression != nil do
      │                                       ~
      │
      └─ lib/ash/data_layer/ets/ets.ex:2243:39: Ash.DataLayer.Ets.log_destroy_query/2
```

### Ash #18: └─ lib/ash/data_layer/ets/ets.ex:2279:39: Ash.DataLayer.Ets.log_update_query/3

- Message: comparison between distinct types found:

```text
      warning: comparison between distinct types found:

          query.filter != nil

      given types:

          dynamic(not false and not nil) != nil

      where "query" was given the types:

          # type: dynamic(%{..., limit: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2258:16
          query.limit

          # type: dynamic(%{..., limit: term(), offset: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2265:16
          query.offset

          # type: dynamic(%{..., limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2272:16
          query.sort

          # type: dynamic(%{..., filter: term(), limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2279:16
          query.filter

          # type: dynamic(%{..., filter: not false and not nil, limit: term(), offset: term(), sort: term()})
          # from: lib/ash/data_layer/ets/ets.ex:2279:16
          query.filter

      While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

      type warning found at:
      │
 2279 │       if query.filter && query.filter != nil && query.filter.expression != nil do
      │                                       ~
      │
      └─ lib/ash/data_layer/ets/ets.ex:2279:39: Ash.DataLayer.Ets.log_update_query/3
```

### Ash #19: └─ lib/ash/resource/change/increment.ex:18:19: Ash.Resource.Change.Increment.change/3

- Message: incompatible types given to Kernel.+/2:

```text
    warning: incompatible types given to Kernel.+/2:

        Map.get(
          changeset.data,
          opts[:attribute]
        ) + opts[:amount]

    given types:

        (
          -dynamic(not nil and not float() and not integer()) or nil- or
          dynamic(float() or integer()),
          dynamic()
        )

    but expected one of:

        #1
        integer(), integer()

        #2
        integer(), float()

        #3
        float(), integer()

        #4
        float(), float()

    where "changeset" was given the type:

        # type: dynamic(%{..., data: map()})
        # from: lib/ash/resource/change/increment.ex:17:16
        Map.get(
          changeset.data,
          opts[:attribute]
        )

    where "opts" was given the type:

        # type: dynamic(
          %{..., __struct__: atom()} or nil or empty_list() or non_empty_list(term(), term()) or
            non_struct_map()
        )
        # from: lib/ash/resource/change/increment.ex:17:24
        opts[:attribute]

    type warning found at:
    │
 18 │         |> Kernel.+(opts[:amount])
    │                   ~
    │
    └─ lib/ash/resource/change/increment.ex:18:19: Ash.Resource.Change.Increment.change/3
```

### Ash #20: └─ lib/ash/actions/read/read.ex:3779: Ash.Actions.Read.do_add_field_level_auth/3

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          is_map(state)

      will always evaluate to:

          true

      where "state" was given the type:

          # type: dynamic(map())
          # from: lib/ash/actions/read/read.ex:3761:13
          state =
            Ash.Authorizer.initial_state(
              authorizer,
              opts[:actor],
              query.resource,
              query.action,
              query.domain
            )

      type warning found at:
      │
 3779 │           is_map(state) && !Map.has_key?(state, :subject) ->
      │           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/actions/read/read.ex:3779: Ash.Actions.Read.do_add_field_level_auth/3
```

### Ash #21: └─ lib/ash/changeset/changeset.ex:4043:13: Ash.Changeset.add_atomic_validations/3

- Message: the following clause will never match:

```text
      warning: the following clause will never match:

          {:expr, {:ok, false}, _expr} ->

      it is expected to match on type:

          dynamic({:expr, term(), term()} and not {:expr, {:ok, term()}, term()})

      type warning found at:
      │
 4043 │             {:expr, {:ok, false}, _expr} ->
      │             ~
      │
      └─ lib/ash/changeset/changeset.ex:4043:13: Ash.Changeset.add_atomic_validations/3
```

### Ash #22: └─ lib/ash/changeset/changeset.ex:2053: Ash.Changeset.for_create/4

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          action

      will always evaluate to:

          dynamic(not false and not nil)

      where "action" was given the type:

          # type: dynamic(not false and not nil)
          # from: lib/ash/changeset/changeset.ex:2047:12
          action =
            get_action_entity(changeset.resource, action) ||
              raise_no_action(changeset.resource, action, :create)

      type warning found at:
      │
 2053 │         nil -> action && action.upsert_condition
      │         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/changeset/changeset.ex:2053: Ash.Changeset.for_create/4
```

### Ash #23: └─ lib/ash/changeset/changeset.ex:172: Inspect.Ash.Changeset.inspect/2

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         changeset.action

     will always evaluate to:

         dynamic(not false and not nil)

     where "changeset" was given the types:

         # type: dynamic(%Ash.Changeset{})
         # from: lib/ash/changeset/changeset.ex:110:17
         changeset

         # type: dynamic(%Ash.Changeset{context: map()})
         # from: lib/ash/changeset/changeset.ex:111:21
         Map.delete(changeset.context, :private)

         # type: dynamic(%Ash.Changeset{tenant: term(), context: map()})
         # from: lib/ash/changeset/changeset.ex:121:22
         changeset.tenant

         # type: dynamic(%Ash.Changeset{domain: term(), tenant: term(), context: map()})
         # from: lib/ash/changeset/changeset.ex:131:22
         changeset.domain

         # type: dynamic(%Ash.Changeset{domain: term(), tenant: term(), context: map(), select: term()})
         # from: lib/ash/changeset/changeset.ex:138:22
         changeset.select

         # type: dynamic(%Ash.Changeset{
           domain: term(),
           tenant: term(),
           context: map(),
           select: term(),
           load: term()
         })
         # from: lib/ash/changeset/changeset.ex:145:22
         changeset.load

         # type: dynamic(%Ash.Changeset{
           domain: term(),
           tenant: term(),
           filter: term(),
           context: map(),
           select: term(),
           load: term()
         })
         # from: lib/ash/changeset/changeset.ex:159:24
         changeset.filter

         # type: dynamic(%Ash.Changeset{
           action: not false and not nil,
           domain: term(),
           tenant: term(),
           filter: term(),
           context: map(),
           select: term(),
           load: term()
         })
         # from: lib/ash/changeset/changeset.ex:171:22
         changeset.action

     type warning found at:
     │
 172 │           concat("action: ", inspect(changeset.action && changeset.action.name))
     │           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/changeset/changeset.ex:172: Inspect.Ash.Changeset.inspect/2
```

### Ash #24: └─ lib/ash/changeset/changeset.ex:2261: Ash.Changeset.for_destroy/4

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          action

      will always evaluate to:

          dynamic(not false and not nil)

      where "action" was given the type:

          # type: dynamic(not false and not nil)
          # from: lib/ash/changeset/changeset.ex:2247:12
          action =
            get_action_entity(changeset.resource, action_or_name) ||
              raise_no_action(changeset.resource, action_or_name, :destroy)

      type warning found at:
      │
 2261 │       if action do
      │       ~~~~~~~~~~~~
      │
      └─ lib/ash/changeset/changeset.ex:2261: Ash.Changeset.for_destroy/4
```

### Ash #25: └─ lib/ash/filter/runtime.ex:414: Ash.Filter.Runtime.resolve_expr/5

- Message: comparison between distinct types found:

```text
     warning: comparison between distinct types found:

         left_resolved == nil

     given types:

         dynamic(not false and not nil) == nil

     where "left_resolved" was given the types:

         # type: dynamic(not false and not nil)
         # from: lib/ash/filter/runtime.ex:409:70
         {:ok, left_resolved} when not (left_resolved === nil or left_resolved === false) <-
           resolve_expr(left, record, parent, resource, unknown_on_unknown_refs?)

         # type: not false and not nil
         # from: lib/ash/filter/runtime.ex:409
         left_resolved in [nil, false]

     While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

     type warning found at:
     │
 414 │         is_nil(left_resolved) ->
     │         ~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/filter/runtime.ex:414: Ash.Filter.Runtime.resolve_expr/5
```

### Ash #26: └─ lib/ash/filter/runtime.ex:438:23: Ash.Filter.Runtime.resolve_expr/5

- Message: this clause in cond will never match:

```text
     warning: this clause in cond will never match:

         left_resolved

     since it has type:

         dynamic(false or nil)

     where "left_resolved" was given the types:

         # type: dynamic(false or nil)
         # from: lib/ash/filter/runtime.ex:433:66
         {:ok, left_resolved} when left_resolved === nil or left_resolved === false <-
           resolve_expr(left, record, parent, resource, unknown_on_unknown_refs?)

         # type: false or nil
         # from: lib/ash/filter/runtime.ex:433
         left_resolved in [nil, false]

     type warning found at:
     │
 438 │         left_resolved ->
     │                       ~
     │
     └─ lib/ash/filter/runtime.ex:438:23: Ash.Filter.Runtime.resolve_expr/5
```

### Ash #27: └─ lib/ash/actions/create/bulk.ex:921: Ash.Actions.Create.Bulk.map_batches/5

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         max_concurrency

     will always evaluate to:

         dynamic(not false and not nil)

     where "max_concurrency" was given the type:

         # type: dynamic(not false and not nil)
         # from: lib/ash/actions/create/bulk.ex:914:21
         max_concurrency =
           if max_concurrency && max_concurrency > 1 && Ash.DataLayer.can?(:async_engine, resource) do
             max_concurrency
           else
             0
           end

     type warning found at:
     │
 921 │     if max_concurrency && max_concurrency > 1 do
     │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/actions/create/bulk.ex:921: Ash.Actions.Create.Bulk.map_batches/5
```

### Ash #28: └─ lib/ash/query/query.ex:573:37: Ash.Query.sort_input/3

- Message: incompatible types given to Kernel.++/2:

```text
     warning: incompatible types given to Kernel.++/2:

         validated ++ query.sort

     given types:

         dynamic() or nil, dynamic(not empty_list())

     but expected one of:

         #1
         empty_list(), term()

         #2
         non_empty_list(term()), term()

     where "query" was given the types:

         # type: dynamic(%Ash.Query{} or %{..., __struct__: Ash.Query} or %{..., resource: term()})
         # from: lib/ash/query/query.ex:556:11
         query = new(query)

         # type: dynamic(
           %Ash.Query{resource: term()} or %{..., __struct__: Ash.Query, resource: term()} or
             %{..., resource: term()}
         )
         # from: lib/ash/query/query.ex:561:24
         Ash.DataLayer.data_layer_can?(query.resource, :sort)

         # type: dynamic(
           %Ash.Query{resource: term(), sort: not empty_list()} or
             %{..., __struct__: Ash.Query, resource: term(), sort: not empty_list()} or
             %{..., resource: term(), sort: not empty_list()}
         )
         # from: lib/ash/query/query.ex:562:42
         query.sort != []

         # type: dynamic(
           %Ash.Query{resource: term(), sort: not empty_list()} or
             %{
               ...,
               __struct__: Ash.Query,
               resource: term(),
               sort: not empty_list(),
               sort_input_indices: term()
             } or %{..., resource: term(), sort: not empty_list(), sort_input_indices: term()}
         )
         # from: lib/ash/query/query.ex:571:20
         Enum.map(query.sort_input_indices, &(&1 + 1))

     where "validated" was given the type:

         # type: dynamic() or nil
         # from: lib/ash/query/query.ex:563:21
         validated =
           Map.get(
             sort_input(
               Map.put(query, :sort, []),
               sorts
             ),
             :sort
           )

     type warning found at:
     │
 573 │           %{query | sort: validated ++ query.sort, sort_input_indices: new_sort_input_indices}
     │                                     ~
     │
     └─ lib/ash/query/query.ex:573:37: Ash.Query.sort_input/3
```

### Ash #29: └─ lib/ash/filter/runtime.ex:439: Ash.Filter.Runtime.resolve_expr/5

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         !!left_resolved

     will always evaluate to false because its inner expression has type:

         dynamic(false or nil)

     type warning found at:
     │
 439 │           {:ok, !!left_resolved}
     │           ~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/filter/runtime.ex:439: Ash.Filter.Runtime.resolve_expr/5
```

### Ash #30: └─ lib/ash/query/function/ago.ex:59:12: Ash.Query.Function.Ago.datetime_add/3

- Message: incompatible types given to Kernel.div/2:

```text
    warning: incompatible types given to Kernel.div/2:

        div(months_since_zero, 12)

    given types:

        -float()- or integer(), integer()

    but expected one of:

        integer(), integer()

    where "months_since_zero" was given the type:

        # type: float() or integer()
        # from: lib/ash/query/function/ago.ex:58:23
        months_since_zero = datetime.year * 12 + datetime.month - 1 + amount_to_add

    type warning found at:
    │
 59 │     year = div(months_since_zero, 12)
    │            ~
    │
    └─ lib/ash/query/function/ago.ex:59:12: Ash.Query.Function.Ago.datetime_add/3
```

### Ash #31: └─ lib/ash/filter/runtime.ex:939: Ash.Filter.Runtime.resolve_ref/5

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
     warning: the following clause cannot match because the previous clauses already matched all possible values:

         _ ->

     it attempts to match on the result of:

         unknown_on_unknown_refs?

     which has the already matched type:

         dynamic(false or nil)

     type warning found at:
     │
 939 │               if unknown_on_unknown_refs? do
     │               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/filter/runtime.ex:939: Ash.Filter.Runtime.resolve_ref/5
```

### Ash #32: └─ lib/ash/actions/helpers.ex:69:72: Ash.Actions.Helpers.split_and_run_simple/7

- Message: incompatible types given to Map.get/2:

```text
    warning: incompatible types given to Map.get/2:

        Map.get(Map.get(changeset.context, context_key), :index)

    given types:

        dynamic() or nil, :index

    but expected one of:

        map(), term()

    where "changeset" was given the type:

        # type: dynamic(%{..., context: map()})
        # from: lib/ash/actions/helpers.ex:69:48
        Map.get(changeset.context, context_key)

    where "context_key" was given the type:

        # type: dynamic()
        # from: lib/ash/actions/helpers.ex:18:71
        context_key

    type warning found at:
    │
 69 │               index = changeset.context |> Map.get(context_key) |> Map.get(:index)
    │                                                                        ~
    │
    └─ lib/ash/actions/helpers.ex:69:72: Ash.Actions.Helpers.split_and_run_simple/7
```

### Ash #33: └─ lib/ash/query/query.ex:4223:41: Ash.Query.sort/3

- Message: incompatible types given to Kernel.++/2:

```text
      warning: incompatible types given to Kernel.++/2:

          validated ++ query.sort

      given types:

          dynamic() or nil, dynamic(not empty_list())

      but expected one of:

          #1
          empty_list(), term()

          #2
          non_empty_list(term()), term()

      where "query" was given the types:

          # type: dynamic(%Ash.Query{} or %{..., __struct__: Ash.Query} or %{..., resource: term()})
          # from: lib/ash/query/query.ex:4205:11
          query = new(query)

          # type: dynamic(%Ash.Query{} or %{..., resource: term()})
          # from: lib/ash/query/query.ex:4210:29
          Ash.Actions.Sort.process(query.resource, sorts)

          # type: dynamic(%Ash.Query{resource: term()} or %{..., resource: term()})
          # from: lib/ash/query/query.ex:4212:28
          Ash.DataLayer.data_layer_can?(query.resource, :sort)

          # type: dynamic(
            %Ash.Query{resource: term(), sort: not empty_list()} or
              %{..., resource: term(), sort: not empty_list()}
          )
          # from: lib/ash/query/query.ex:4213:46
          query.sort != []

          # type: dynamic(
            %Ash.Query{resource: term(), sort: not empty_list()} or
              %{..., resource: term(), sort: not empty_list(), sort_input_indices: term()}
          )
          # from: lib/ash/query/query.ex:4221:22
          Enum.map(query.sort_input_indices, &(&1 + 1))

      where "validated" was given the type:

          # type: dynamic() or nil
          # from: lib/ash/query/query.ex:4214:25
          validated =
            Map.get(
              sort(
                Map.put(query, :sort, []),
                sorts
              ),
              :sort
            )

      type warning found at:
      │
 4223 │               %{query | sort: validated ++ query.sort, sort_input_indices: new_sort_input_indices}
      │                                         ~
      │
      └─ lib/ash/query/query.ex:4223:41: Ash.Query.sort/3
```

### Ash #34: └─ lib/ash/query/query.ex:2084:15: Ash.Query.load_through/4

- Message: expected a map or struct when accessing .type in expression:

```text
      warning: expected a map or struct when accessing .type in expression:

          calc.type

      where "calc" was given the type:

          # type: dynamic() or nil
          # from: lib/ash/query/query.ex:2083:14
          calc = Map.get(query.calculations, name)

      hint: "var.field" (without parentheses) means "var" is a map() while "var.fun()" (with parentheses) means "var" is an atom()

      type warning found at:
      │
 2084 │         {calc.type, calc.constraints}
      │               ~
      │
      └─ lib/ash/query/query.ex:2084:15: Ash.Query.load_through/4
```

### Ash #35: └─ lib/ash/subject.ex:205:47: Ash.Subject.get_argument/2

- Message: incompatible types given as default arguments to get_argument/3:

```text
     warning: incompatible types given as default arguments to get_argument/3:

         (
           -dynamic(not %Ash.ActionInput{} and not %Ash.Changeset{} and not %Ash.Query{})-,
           dynamic(atom() or binary()),
           nil
         )

     but expected one of:

         %Ash.ActionInput{} or %Ash.Changeset{} or %Ash.Query{}, atom() or binary(), term()

     where "x0" (context :elixir_def) was given the type:

         # type: dynamic(not %Ash.ActionInput{} and not %Ash.Changeset{} and not %Ash.Query{})
         # from: lib/ash/subject.ex
         x0

     where "x1" (context :elixir_def) was given the types:

         # type: dynamic(atom() or binary())
         # from: lib/ash/subject.ex:205:47
         super(x0, x1, nil)

         # type: dynamic()
         # from: lib/ash/subject.ex
         x1

     type warning found at:
     │
 205 │   def get_argument(subject, argument, default \\ nil) do
     │                                               ~
     │
     └─ lib/ash/subject.ex:205:47: Ash.Subject.get_argument/2
```

### Ash #36: └─ lib/ash/actions/read/calculations.ex:241: Ash.Actions.Read.Calculations.calculate/3

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
     warning: the following clause cannot match because the previous clauses already matched all possible values:

         _ ->

     it attempts to match on the result of:

         primary_key

     which has the already matched type:

         dynamic(false or nil)

     type warning found at:
     │
 241 │               if primary_key do
     │               ~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/actions/read/calculations.ex:241: Ash.Actions.Read.Calculations.calculate/3
```

### Ash #37: └─ lib/ash/actions/read/calculations.ex:327:18: Ash.Actions.Read.Calculations.replace_refs/2

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
     warning: the following clause cannot match because the previous clauses already matched all possible values:

         name ->

     it attempts to match on the result of:

         attribute

     which has the already matched type:

         dynamic(%Ash.Resource.Attribute{})

     where "name" was given the type:

         # type: dynamic(%Ash.Resource.Attribute{})
         # from: lib/ash/actions/read/calculations.ex:327:13
         name

     type warning found at:
     │
 327 │             name -> name
     │                  ~
     │
     └─ lib/ash/actions/read/calculations.ex:327:18: Ash.Actions.Read.Calculations.replace_refs/2
```

### Ash #38: └─ lib/ash/type/union.ex:850:25: Ash.Type.Union.tags_equal?/2

- Message: comparison between distinct types found:

```text
     warning: comparison between distinct types found:

         their_tag_value == tag_value

     given types:

         dynamic(atom()) == binary()

     where "tag_value" was given the types:

         # type: dynamic(not atom())
         # from: lib/ash/type/union.ex:846:7
         is_atom(tag_value)

         # type: binary()
         # from: lib/ash/type/union.ex:849:7
         is_binary(tag_value)

     where "their_tag_value" was given the type:

         # type: dynamic(atom())
         # from: lib/ash/type/union.ex:849:31
         is_atom(their_tag_value)

     While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

     type warning found at:
     │
 850 │         their_tag_value == tag_value || to_string(their_tag_value) == tag_value
     │                         ~
     │
     └─ lib/ash/type/union.ex:850:25: Ash.Type.Union.tags_equal?/2
```

### Ash #39: └─ lib/ash/expr/expr.ex:1260: Ash.Expr.determine_types/4

- Message: the following clause will never match:

```text
      warning: the following clause will never match:

          {type, constraints} ->

      because it attempts to match on the result of:

          type

      which has type:

          empty_list()

      type warning found at:
      │
 1260 │                   {type, constraints} ->
      │                   ~~~~~~~~~~~~~~~~~~~~~~
      │
      └─ lib/ash/expr/expr.ex:1260: Ash.Expr.determine_types/4
```

### Ash #40: └─ lib/ash/type/union.ex:1088:39: Ash.Type.Union.prepare_change_array/3

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(union, :__index__)

      the map:

          dynamic(%Ash.Union{})

      does not have all required keys:

          :__index__

      therefore this function will always return nil

      where "union" was given the type:

          # type: dynamic(%Ash.Union{})
          # from: lib/ash/type/union.ex:1087:36
          %Ash.Union{value: value} = union

      type warning found at:
      │
 1088 │             {:union_value, value, Map.get(union, :__index__)}
      │                                       ~
      │
      └─ lib/ash/type/union.ex:1088:39: Ash.Type.Union.prepare_change_array/3
```

### Ash #41: └─ lib/ash/query/query.ex:2549: Ash.Query.validate_calculation_arguments/3

- Message: the following conditional expression:

```text
      warning: the following conditional expression:

          !argument

      will always evaluate to false because its inner expression has type:

          dynamic(%{..., type: term()})

      where "argument" was given the type:

          # type: dynamic(%{..., type: term()})
          # from: lib/ash/query/query.ex:2546:32
          Ash.Type.Helpers.handle_indexed_maps(argument.type, value)

      type warning found at:
      │
 2549 │         !argument ->
      │         ~~~~~~~~~~~~
      │
      └─ lib/ash/query/query.ex:2549: Ash.Query.validate_calculation_arguments/3
```

### Ash #42: └─ lib/ash/query/query.ex:372: Inspect.Ash.Query.arguments/2

- Message: comparison between distinct types found:

```text
     warning: comparison between distinct types found:

         query.action == nil

     given types:

         dynamic(not false and not nil) == nil

     where "query" was given the types:

         # type: dynamic(%{..., action: term()})
         # from: lib/ash/query/query.ex:371:16
         query.action

         # type: dynamic(%{..., action: not false and not nil})
         # from: lib/ash/query/query.ex:371:16
         query.action

     While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

     type warning found at:
     │
 372 │         if is_nil(query.action) || Enum.empty?(query.action.arguments) do
     │         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/ash/query/query.ex:372: Inspect.Ash.Query.arguments/2
```

### Ash #43: └─ lib/ash/sort/sort.ex:469: Ash.Sort.related_field/6

- Message: the following clause will never match:

```text
     warning: the following clause will never match:

         {:ok, nil} ->

     because it attempts to match on the result of:

         do_get_field(resource, field, only_public?, input)

     which has type:

         dynamic(
           ({...} and not {:ok, term()} and
              not {:ok,
               %Ash.Query.Calculation{
                 load: nil,
                 context: %Ash.Resource.Calculation.Context{domain: nil, resource: nil},
                 select: empty_list()
               }}) or atom() or bitstring() or empty_list() or float() or fun() or integer() or map() or
             non_empty_list(term(), term()) or pid() or port() or reference() or
             {:error, %{..., __struct__: atom()} or %{..., __struct__: term(), vars: term()}} or
             {:ok,
              %Ash.Query.Aggregate{} or %Ash.Query.Calculation{} or (atom() and not nil) or
                (map() and not %Ash.Resource.Calculation{}) or bitstring() or empty_list() or float() or
                fun() or integer() or non_empty_list(term(), term()) or pid() or port() or reference() or
                {...}}
         )

     type warning found at:
     │
 469 │       {:ok, nil} ->
     │       ~~~~~~~~~~~~~
     │
     └─ lib/ash/sort/sort.ex:469: Ash.Sort.related_field/6
```

### Ash #44: └─ lib/ash/resource/info.ex:1007:57: Ash.Resource.Info.synonymous_relationship_paths?/4

- Message: incompatible types given to Kernel.++/2:

```text
      warning: incompatible types given to Kernel.++/2:

          Map.get(relationship, :through) ++ rest

      given types:

          dynamic() or nil, dynamic()

      but expected one of:

          #1
          empty_list(), term()

          #2
          non_empty_list(term()), term()

      where "relationship" was given the types:

          # type: dynamic()
          # from: lib/ash/resource/info.ex:1003:8
          relationship

          # type: dynamic(not false and not nil)
          # from: lib/ash/resource/info.ex:1003:8
          relationship

          # type: dynamic(map())
          # from: lib/ash/resource/info.ex:1006:19
          Map.get(relationship, :through)

      where "rest" was given the type:

          # type: dynamic()
          # from: lib/ash/resource/info.ex
          [first | rest]

      type warning found at:
      │
 1007 │         expanded_path = Map.get(relationship, :through) ++ rest
      │                                                         ~
      │
      └─ lib/ash/resource/info.ex:1007:57: Ash.Resource.Info.synonymous_relationship_paths?/4
```

### Ash #45: └─ lib/ash/error/invalid/no_matching_bulk_strategy.ex:33: Ash.Error.Invalid.NoMatchingBulkStrategy."message (overridable 1)"/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        action

    will always evaluate to:

        dynamic(not atom())

    where "action" was given the type:

        # type: dynamic(not atom())
        # from: lib/ash/error/invalid/no_matching_bulk_strategy.ex:30:10
        is_atom(action)

    type warning found at:
    │
 33 │         action && action.name
    │         ~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/ash/error/invalid/no_matching_bulk_strategy.ex:33: Ash.Error.Invalid.NoMatchingBulkStrategy."message (overridable 1)"/1
```

## Blockscout (50)

### Blockscout #1: └─ (ethereum_jsonrpc 11.0.3) lib/ethereum_jsonrpc/decode_error.ex:58:20: EthereumJSONRPC.DecodeError.message/1

- Message: incompatible types given to Map.get/3:

```text
    warning: incompatible types given to Map.get/3:

        Map.get(decode_error, :hide_url, false)

    the map:

        dynamic(%EthereumJSONRPC.DecodeError{
          request: %EthereumJSONRPC.DecodeError.Request{},
          response: %EthereumJSONRPC.DecodeError.Response{}
        })

    does not have all required keys:

        :hide_url

    therefore this function will always return false

    where "decode_error" was given the type:

        # type: dynamic(%EthereumJSONRPC.DecodeError{
          request: %EthereumJSONRPC.DecodeError.Request{},
          response: %EthereumJSONRPC.DecodeError.Response{}
        })
        # from: lib/ethereum_jsonrpc/decode_error.ex:46:11
        %EthereumJSONRPC.DecodeError{
          request: %EthereumJSONRPC.DecodeError.Request{
            url: request_url,
            body: request_body,
            headers: headers
          },
          response: %EthereumJSONRPC.DecodeError.Response{
            status_code: response_status_code,
            body: response_body
          }
        } = decode_error

    type warning found at:
    │
 58 │     hide_url = Map.get(decode_error, :hide_url, false)
    │                    ~
    │
    └─ (ethereum_jsonrpc 11.0.3) lib/ethereum_jsonrpc/decode_error.ex:58:20: EthereumJSONRPC.DecodeError.message/1
```

### Blockscout #2: └─ (explorer 11.0.3) lib/release_tasks.ex:88:14: Explorer.ReleaseTasks.run_migrations_for/1

- Message: incompatible types given to Ecto.Migrator.run/4:

```text
    warning: incompatible types given to Ecto.Migrator.run/4:

        Ecto.Migrator.run(repo, migrations_path, :up, all: true)

    given types:

        (
          -dynamic(%{..., config: empty_list() or non_empty_list(term(), term())})-,
          dynamic(),
          :up,
          non_empty_list({:all, true})
        )

    but expected one of:

        atom(), term(), term(), empty_list() or non_empty_list(term(), term())

    where "migrations_path" was given the type:

        # type: dynamic()
        # from: lib/release_tasks.ex:87:21
        migrations_path = priv_path_for(repo, "migrations")

    where "repo" was given the type:

        # type: dynamic(%{..., config: empty_list() or non_empty_list(term(), term())})
        # from: lib/release_tasks.ex:85:19
        Keyword.get(repo.config, :otp_app)

    type warning found at:
    │
 88 │     Migrator.run(repo, migrations_path, :up, all: true)
    │              ~
    │
    └─ (explorer 11.0.3) lib/release_tasks.ex:88:14: Explorer.ReleaseTasks.run_migrations_for/1
```

### Blockscout #3: └─ (explorer 11.0.3) lib/explorer/account/notifier/notify.ex:157:35: Explorer.Account.Notifier.Notify.watched?/3

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(address, :watch_zrc_2_input)

     the map:

         dynamic(%Explorer.Account.WatchlistAddress{})

     does not have all required keys:

         :watch_zrc_2_input

     therefore this function will always return nil

     where "address" was given the type:

         # type: dynamic(%Explorer.Account.WatchlistAddress{})
         # from: lib/explorer/account/notifier/notify.ex:145:37
         %Explorer.Account.WatchlistAddress{} = address

     type warning found at:
     │
 157 │       {"ZRC-2", :incoming} -> Map.get(address, :watch_zrc_2_input)
     │                                   ~
     │
     └─ (explorer 11.0.3) lib/explorer/account/notifier/notify.ex:157:35: Explorer.Account.Notifier.Notify.watched?/3
```

### Blockscout #4: └─ (explorer 11.0.3) lib/explorer/account/notifier/notify.ex:158:35: Explorer.Account.Notifier.Notify.watched?/3

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(address, :watch_zrc_2_output)

     the map:

         dynamic(%Explorer.Account.WatchlistAddress{})

     does not have all required keys:

         :watch_zrc_2_output

     therefore this function will always return nil

     where "address" was given the type:

         # type: dynamic(%Explorer.Account.WatchlistAddress{})
         # from: lib/explorer/account/notifier/notify.ex:145:37
         %Explorer.Account.WatchlistAddress{} = address

     type warning found at:
     │
 158 │       {"ZRC-2", :outgoing} -> Map.get(address, :watch_zrc_2_output)
     │                                   ~
     │
     └─ (explorer 11.0.3) lib/explorer/account/notifier/notify.ex:158:35: Explorer.Account.Notifier.Notify.watched?/3
```

### Blockscout #5: └─ (explorer 11.0.3) lib/release_tasks.ex:111:17: Explorer.ReleaseTasks.priv_path_for/2

- Message: incompatible types given to Module.split/1:

```text
     warning: incompatible types given to Module.split/1:

         Module.split(repo)

     given types:

         -dynamic(%{..., config: empty_list() or non_empty_list(term(), term())})-

     but expected one of:

         atom() or binary()

     where "repo" was given the type:

         # type: dynamic(%{..., config: empty_list() or non_empty_list(term(), term())})
         # from: lib/release_tasks.ex:107:19
         Keyword.get(repo.config, :otp_app)

     type warning found at:
     │
 111 │       |> Module.split()
     │                 ~
     │
     └─ (explorer 11.0.3) lib/release_tasks.ex:111:17: Explorer.ReleaseTasks.priv_path_for/2
```

### Blockscout #6: └─ (explorer 11.0.3) lib/explorer/chain/fhe/fhe_contract_checker.ex:32: Explorer.Chain.FheContractChecker.check_and_save_fhe_status/2

- Message: comparison between distinct types found:

```text
    warning: comparison between distinct types found:

        address.contract_code == nil

    given types:

        dynamic(not nil) == nil

    where "address" was given the types:

        # type: dynamic(
          %Explorer.Chain.Address{contract_code: term()} or
            (map() and not (%Explorer.Chain.Address{} or %Ecto.Association.NotLoaded{})) or atom() or
            bitstring() or empty_list() or float() or fun() or integer() or non_empty_list(term(), term()) or
            pid() or port() or reference() or {...}
        )
        # from: lib/explorer/chain/fhe/fhe_contract_checker.ex:32:19
        Explorer.Chain.Address.smart_contract?(address)

        # type: dynamic(%Explorer.Chain.Address{contract_code: not nil})
        # from: lib/explorer/chain/fhe/fhe_contract_checker.ex:32:19
        Explorer.Chain.Address.smart_contract?(address)

    While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

    type warning found at:
    │
 32 │       not Address.smart_contract?(address) or is_nil(address.contract_code) -> :empty
    │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (explorer 11.0.3) lib/explorer/chain/fhe/fhe_contract_checker.ex:32: Explorer.Chain.FheContractChecker.check_and_save_fhe_status/2
```

### Blockscout #7: └─ (explorer 11.0.3) lib/explorer/third_party_integrations/sourcify.ex:362:75: Explorer.ThirdPartyIntegrations.Sourcify.parse_json_from_sourcify_for_insertion/1

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(Map.get(content_json, "compiler"), "version")

     given types:

         dynamic() or nil, binary()

     but expected one of:

         map(), term()

     where "content_json" was given the type:

         # type: dynamic(map())
         # from: lib/explorer/third_party_integrations/sourcify.ex:362:52
         Map.get(content_json, "compiler")

     type warning found at:
     │
 362 │     compiler_version = "v" <> (content_json |> Map.get("compiler") |> Map.get("version"))
     │                                                                           ~
     │
     └─ (explorer 11.0.3) lib/explorer/third_party_integrations/sourcify.ex:362:75: Explorer.ThirdPartyIntegrations.Sourcify.parse_json_from_sourcify_for_insertion/1
```

### Blockscout #8: └─ (explorer 11.0.3) lib/explorer/third_party_integrations/universal_proxy.ex:99: Explorer.ThirdPartyIntegrations.UniversalProxy.api_request_inner/1

- Message: comparison between distinct types found:

```text
    warning: comparison between distinct types found:

        method == nil

    given types:

        dynamic(not nil) == nil

    where "method" was given the types:

        # type: dynamic(not nil)
        # from: lib/explorer/third_party_integrations/universal_proxy.ex:91:26
        %{url: url, body: body, headers: headers, method: method, protocol: protocol}

        # type: not nil
        # from: lib/explorer/third_party_integrations/universal_proxy.ex:98
        method == nil

    While Elixir can compare across all types, you are comparing across types which are always disjoint, and the result is either always true or always false

    type warning found at:
    │
 99 │     with {:invalid_config, false} <- {:invalid_config, is_nil(method)},
    │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (explorer 11.0.3) lib/explorer/third_party_integrations/universal_proxy.ex:99: Explorer.ThirdPartyIntegrations.UniversalProxy.api_request_inner/1
```

### Blockscout #9: └─ (explorer 11.0.3) lib/explorer/third_party_integrations/universal_proxy.ex:228:70: Explorer.ThirdPartyIntegrations.UniversalProxy.parse_protocol/1

- Message: incompatible types given to String.to_atom/1:

```text
     warning: incompatible types given to String.to_atom/1:

         String.to_atom(Map.get(URI.parse(base_url), :scheme))

     given types:

         -dynamic(not nil and not binary()) or nil- or binary()

     but expected one of:

         binary()

     where "base_url" was given the type:

         # type: dynamic(%URI{} or binary())
         # from: lib/explorer/third_party_integrations/universal_proxy.ex:228:32
         URI.parse(base_url)

     type warning found at:
     │
 228 │     protocol = base_url |> URI.parse() |> Map.get(:scheme) |> String.to_atom()
     │                                                                      ~
     │
     └─ (explorer 11.0.3) lib/explorer/third_party_integrations/universal_proxy.ex:228:70: Explorer.ThirdPartyIntegrations.UniversalProxy.parse_protocol/1
```

### Blockscout #10: └─ (explorer 11.0.3) lib/explorer/smart_contract/solidity/publisher_worker.ex:9: Explorer.SmartContract.Solidity.PublisherWorker.__after_compile__/2

- Message: the following conditional expression will always succeed:

```text
    warning: the following conditional expression will always succeed:

        is_integer(5)

    because it evaluates to:

        true

    type warning found at:
    │
  9 │   use Que.Worker, concurrency: 5
    │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (explorer 11.0.3) lib/explorer/smart_contract/solidity/publisher_worker.ex:9: Explorer.SmartContract.Solidity.PublisherWorker.__after_compile__/2
```

### Blockscout #11: └─ (explorer 11.0.3) lib/explorer/smart_contract/stylus/publisher_worker.ex:15: Explorer.SmartContract.Stylus.PublisherWorker.__after_compile__/2

- Message: the following conditional expression will always succeed:

```text
    warning: the following conditional expression will always succeed:

        is_integer(5)

    because it evaluates to:

        true

    type warning found at:
    │
 15 │   use Que.Worker, concurrency: 5
    │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (explorer 11.0.3) lib/explorer/smart_contract/stylus/publisher_worker.ex:15: Explorer.SmartContract.Stylus.PublisherWorker.__after_compile__/2
```

### Blockscout #12: └─ (explorer 11.0.3) lib/explorer/smart_contract/vyper/publisher_worker.ex:9: Explorer.SmartContract.Vyper.PublisherWorker.__after_compile__/2

- Message: the following conditional expression will always succeed:

```text
    warning: the following conditional expression will always succeed:

        is_integer(5)

    because it evaluates to:

        true

    type warning found at:
    │
  9 │   use Que.Worker, concurrency: 5
    │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (explorer 11.0.3) lib/explorer/smart_contract/vyper/publisher_worker.ex:9: Explorer.SmartContract.Vyper.PublisherWorker.__after_compile__/2
```

### Blockscout #13: └─ (explorer 11.0.3) lib/explorer/chain/transaction.ex:2173:31: Explorer.Chain.Transaction.operator_fee/1

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(transaction, :operator_fee_scalar)

      the map:

          dynamic(%Explorer.Chain.Transaction{})

      does not have all required keys:

          :operator_fee_scalar

      therefore this function will always return nil

      where "transaction" was given the type:

          # type: dynamic(%Explorer.Chain.Transaction{})
          # from: lib/explorer/chain/transaction.ex:2170:11
          %Explorer.Chain.Transaction{gas: gas, gas_used: gas_used} = transaction

      type warning found at:
      │
 2173 │     operator_fee_scalar = Map.get(transaction, :operator_fee_scalar) || Decimal.new(0)
      │                               ~
      │
      └─ (explorer 11.0.3) lib/explorer/chain/transaction.ex:2173:31: Explorer.Chain.Transaction.operator_fee/1
```

### Blockscout #14: └─ (explorer 11.0.3) lib/explorer/chain/address/coin_balance.ex:239:39: Explorer.Chain.Address.CoinBalance.address_to_coin_balances_internal/3

- Message: incompatible types given to Kernel.-/2:

```text
     warning: incompatible types given to Kernel.-/2:

         max_block_number - min_block_number

     given types:

         (
           -dynamic(not nil and not float() and not integer()) or nil- or
           dynamic(float() or integer()),
           -dynamic(not nil and not float() and not integer()) or nil- or
           dynamic(float() or integer())
         )

     but expected one of:

         #1
         integer(), integer()

         #2
         integer(), float()

         #3
         float(), integer()

         #4
         float(), float()

     where "max_block_number" was given the type:

         # type: dynamic() or nil
         # from: lib/explorer/chain/address/coin_balance.ex:223:24
         max_block_number =
           Map.get(
             Enum.max_by(balances_raw_filtered, fn balance -> balance.block_number end, fn -> %{} end),
             :block_number
           )

     where "min_block_number" was given the type:

         # type: dynamic() or nil
         # from: lib/explorer/chain/address/coin_balance.ex:218:24
         min_block_number =
           Map.get(
             Enum.min_by(balances_raw_filtered, fn balance -> balance.block_number end, fn -> %{} end),
             :block_number
           )

     type warning found at:
     │
 239 │       blocks_delta = max_block_number - min_block_number
     │                                       ~
     │
     └─ (explorer 11.0.3) lib/explorer/chain/address/coin_balance.ex:239:39: Explorer.Chain.Address.CoinBalance.address_to_coin_balances_internal/3
```

### Blockscout #15: └─ (explorer 11.0.3) lib/explorer/arbitrum/claim_rollup_message.ex:153:11: Explorer.Arbitrum.ClaimRollupMessage.claim_message/1

- Message: the following clause will never match:

```text
     warning: the following clause will never match:

         w when w.status == :initiated ->

     because it attempts to match on the result of:

         log_to_withdrawal(log, message)

     which has type:

         dynamic(
           %Explorer.Arbitrum.Withdraw{
             message_id: integer(),
             status: not :initiated,
             data: binary(),
             token:
               %{
                 address_hash: term(),
                 amount: term(),
                 decimals: term(),
                 destination_address_hash: term(),
                 name: term(),
                 symbol: term()
               } or nil
           } or nil
         )

     where "w" was given the type:

         # type: %{..., status: :initiated}
         # from: lib/explorer/arbitrum/claim_rollup_message.ex:153:27
         w.status == :initiated

     type warning found at:
     │
 153 │           w when w.status == :initiated ->
     │           ~
     │
     └─ (explorer 11.0.3) lib/explorer/arbitrum/claim_rollup_message.ex:153:11: Explorer.Arbitrum.ClaimRollupMessage.claim_message/1
```

### Blockscout #16: └─ (explorer 11.0.3) lib/explorer/chain/import/runner/internal_transactions.ex:718: Explorer.Chain.Import.Runner.InternalTransactions.update_transactions_inner_wrapper/10

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         transaction_from_db

     will always evaluate to:

         dynamic(not false and not nil)

     where "transaction_from_db" was given the types:

         # type: dynamic()
         # from: lib/explorer/chain/import/runner/internal_transactions.ex:703:8
         transaction_from_db

         # type: dynamic(not false and not nil)
         # from: lib/explorer/chain/import/runner/internal_transactions.ex:703:8
         transaction_from_db

     type warning found at:
     │
 718 │       transaction_from_db && Map.get(transaction_from_db, :cumulative_gas_used) ->
     │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ (explorer 11.0.3) lib/explorer/chain/import/runner/internal_transactions.ex:718: Explorer.Chain.Import.Runner.InternalTransactions.update_transactions_inner_wrapper/10
```

### Blockscout #17: └─ (explorer 11.0.3) lib/explorer/bloom_filter.ex:77:29: Explorer.BloomFilter.get_index/3

- Message: incompatible types given to Kernel.rem/2:

```text
    warning: incompatible types given to Kernel.rem/2:

        rem(Bitwise.bsl(:binary.at(bytes, index_1), 8) + :binary.at(bytes, index_2), 2048)

    given types:

        -float()- or integer(), integer()

    but expected one of:

        integer(), integer()

    where "bytes" was given the type:

        # type: dynamic()
        # from: lib/explorer/bloom_filter.ex:76:18
        bytes

    where "index_1" was given the type:

        # type: dynamic()
        # from: lib/explorer/bloom_filter.ex:76:25
        index_1

    where "index_2" was given the type:

        # type: dynamic()
        # from: lib/explorer/bloom_filter.ex:76:34
        index_2

    type warning found at:
    │
 77 │     @bloom_bit_length - 1 - rem((:binary.at(bytes, index_1) <<< 8) + :binary.at(bytes, index_2), 2048)
    │                             ~
    │
    └─ (explorer 11.0.3) lib/explorer/bloom_filter.ex:77:29: Explorer.BloomFilter.get_index/3
```

### Blockscout #18: └─ (indexer 11.0.3) lib/indexer/fetcher/arbitrum/tracking_batches_statuses.ex:660:5: Indexer.Fetcher.Arbitrum.TrackingBatchesStatuses.rescheduled?/2

- Message: incompatible types given to Kernel.not/1:

```text
     warning: incompatible types given to Kernel.not/1:

         not Map.get(state.completed_tasks, task_tag)

     given types:

         -dynamic(not nil and not boolean()) or nil- or dynamic(boolean())

     but expected one of:

         #1
         true

         #2
         false

     where "state" was given the type:

         # type: dynamic(%{..., completed_tasks: map()})
         # from: lib/indexer/fetcher/arbitrum/tracking_batches_statuses.ex:660:13
         Map.get(state.completed_tasks, task_tag)

     where "task_tag" was given the types:

         # type: dynamic(
           :historical_batches or :historical_confirmations or :historical_executions or :missing_batches
         )
         # from: lib/indexer/fetcher/arbitrum/tracking_batches_statuses.ex:659:21
         task_tag

         # type: :historical_batches or :historical_confirmations or :historical_executions or :missing_batches
         # from: lib/indexer/fetcher/arbitrum/tracking_batches_statuses.ex:659
         task_tag in [
           :historical_batches,
           :missing_batches,
           :historical_confirmations,
           :historical_executions
         ]

     type warning found at:
     │
 660 │     not Map.get(state.completed_tasks, task_tag)
     │     ~
     │
     └─ (indexer 11.0.3) lib/indexer/fetcher/arbitrum/tracking_batches_statuses.ex:660:5: Indexer.Fetcher.Arbitrum.TrackingBatchesStatuses.rescheduled?/2
```

### Blockscout #19: └─ (indexer 11.0.3) lib/indexer/fetcher/arbitrum/tracking_messages_on_l1.ex:420:5: Indexer.Fetcher.Arbitrum.TrackingMessagesOnL1.rescheduled?/2

- Message: incompatible types given to Kernel.not/1:

```text
     warning: incompatible types given to Kernel.not/1:

         not Map.get(state.completed_tasks, task_tag)

     given types:

         -dynamic(not nil and not boolean()) or nil- or dynamic(boolean())

     but expected one of:

         #1
         true

         #2
         false

     where "state" was given the type:

         # type: dynamic(%{..., completed_tasks: map()})
         # from: lib/indexer/fetcher/arbitrum/tracking_messages_on_l1.ex:420:13
         Map.get(state.completed_tasks, task_tag)

     where "task_tag" was given the types:

         # type: dynamic(:check_historical or :check_missing_origination)
         # from: lib/indexer/fetcher/arbitrum/tracking_messages_on_l1.ex:419:21
         task_tag

         # type: :check_historical or :check_missing_origination
         # from: lib/indexer/fetcher/arbitrum/tracking_messages_on_l1.ex:419
         task_tag in [:check_historical, :check_missing_origination]

     type warning found at:
     │
 420 │     not Map.get(state.completed_tasks, task_tag)
     │     ~
     │
     └─ (indexer 11.0.3) lib/indexer/fetcher/arbitrum/tracking_messages_on_l1.ex:420:5: Indexer.Fetcher.Arbitrum.TrackingMessagesOnL1.rescheduled?/2
```

### Blockscout #20: └─ (indexer 11.0.3) lib/indexer/fetcher/token_instance/realtime.ex:81:18: Indexer.Fetcher.TokenInstance.Realtime.async_fetch/2

- Message: incompatible types given to Indexer.BufferedTask.buffer/3:

```text
    warning: incompatible types given to Indexer.BufferedTask.buffer/3:

        Indexer.BufferedTask.buffer(Indexer.Fetcher.TokenInstance.Realtime, data, true)

    given types:

        (
          Indexer.Fetcher.TokenInstance.Realtime,
          -dynamic(not empty_list() and not non_empty_list(term(), term()))-,
          true
        )

    but expected one of:

        (
          atom() or pid() or {:via, atom(), term()} or {atom(), term()},
          empty_list() or non_empty_list(term(), term()),
          term()
        )

    where "data" was given the type:

        # type: dynamic(not empty_list() and not non_empty_list(term(), term()))
        # from: lib/indexer/fetcher/token_instance/realtime.ex:80:19
        data

    type warning found at:
    │
 81 │     BufferedTask.buffer(__MODULE__, data, true)
    │                  ~
    │
    └─ (indexer 11.0.3) lib/indexer/fetcher/token_instance/realtime.ex:81:18: Indexer.Fetcher.TokenInstance.Realtime.async_fetch/2
```

### Blockscout #21: └─ (indexer 11.0.3) lib/indexer/fetcher/zksync/discovery/batches_data.ex:222:25: Indexer.Fetcher.ZkSync.Discovery.BatchesData.request_block_ranges_for_batches/4

- Message: expected a map or struct when accessing .start_block in expression:

```text
     warning: expected a map or struct when accessing .start_block in expression:

         batch.start_block

     where "batch" was given the type:

         # type: dynamic() or nil
         # from: lib/indexer/fetcher/zksync/discovery/batches_data.ex:220:13
         batch = Map.get(batches_src, batch_number)

     hint: "var.field" (without parentheses) means "var" is a map() while "var.fun()" (with parentheses) means "var" is an atom()

     type warning found at:
     │
 222 │       case is_nil(batch.start_block) or is_nil(batch.end_block) do
     │                         ~
     │
     └─ (indexer 11.0.3) lib/indexer/fetcher/zksync/discovery/batches_data.ex:222:25: Indexer.Fetcher.ZkSync.Discovery.BatchesData.request_block_ranges_for_batches/4
```

### Blockscout #22: └─ (indexer 11.0.3) lib/indexer/fetcher/zksync/discovery/batches_data.ex:282:15: Indexer.Fetcher.ZkSync.Discovery.BatchesData.get_l2_blocks_and_transactions/2

- Message: expected a map or struct when accessing .start_block in expression:

```text
     warning: expected a map or struct when accessing .start_block in expression:

         batch.start_block

     where "batch" was given the type:

         # type: dynamic() or nil
         # from: lib/indexer/fetcher/zksync/discovery/batches_data.ex:280:15
         batch = Map.get(batches, batch_number)

     hint: "var.field" (without parentheses) means "var" is a map() while "var.fun()" (with parentheses) means "var" is an atom()

     type warning found at:
     │
 282 │         batch.start_block..batch.end_block
     │               ~
     │
     └─ (indexer 11.0.3) lib/indexer/fetcher/zksync/discovery/batches_data.ex:282:15: Indexer.Fetcher.ZkSync.Discovery.BatchesData.get_l2_blocks_and_transactions/2
```

### Blockscout #23: └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/interop/message_queue.ex:116:36: Indexer.Fetcher.Optimism.Interop.MessageQueue.handle_continue/2

- Message: incompatible types given to Kernel.div/2:

```text
     warning: incompatible types given to Kernel.div/2:

         div(env[:export_expiration] * 24 * 3600, block_duration)

     given types:

         -float()- or integer(), integer()

     but expected one of:

         integer(), integer()

     where "block_duration" was given the type:

         # type: integer()
         # from: lib/indexer/fetcher/optimism/interop/message_queue.ex:99:45
         is_integer(block_duration)

     where "env" was given the type:

         # type: dynamic(
           %{..., __struct__: atom()} or nil or empty_list() or non_empty_list(term(), term()) or
             non_struct_map()
         )
         # from: lib/indexer/fetcher/optimism/interop/message_queue.ex:93:29
         env[:chainscout_api_url]

     type warning found at:
     │
 116 │          export_expiration_blocks: div(env[:export_expiration] * 24 * 3600, block_duration),
     │                                    ~
     │
     └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/interop/message_queue.ex:116:36: Indexer.Fetcher.Optimism.Interop.MessageQueue.handle_continue/2
```

### Blockscout #24: └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1034:25: Indexer.Fetcher.Optimism.TransactionBatch.handle_channel/7

- Message: incompatible types given to Map.get/2:

```text
      warning: incompatible types given to Map.get/2:

          Map.get(frame, :eip4844_blob_hash)

      given types:

          dynamic() or nil, :eip4844_blob_hash

      but expected one of:

          map(), term()

      where "frame" was given the type:

          # type: dynamic() or nil
          # from: lib/indexer/fetcher/optimism/transaction_batch.ex:1028:15
          frame = Map.get(channel.frames, frame_number)

      type warning found at:
      │
 1034 │             !is_nil(Map.get(frame, :eip4844_blob_hash)) ->
      │                         ~
      │
      └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1034:25: Indexer.Fetcher.Optimism.TransactionBatch.handle_channel/7
```

### Blockscout #25: └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1468:43: Indexer.Fetcher.Optimism.TransactionBatch.parent_hash_to_l2_block_number/2

- Message: incompatible types given to Kernel.+/2:

```text
      warning: incompatible types given to Kernel.+/2:

          number + 1

      given types:

          (
            -dynamic(not nil and not float() and not integer()) or nil- or
            dynamic(float() or integer()),
            integer()
          )

      but expected one of:

          #1
          integer(), integer()

          #2
          integer(), float()

          #3
          float(), integer()

          #4
          float(), float()

      where "number" was given the type:

          # type: dynamic() or nil
          # from: lib/indexer/fetcher/optimism/transaction_batch.ex:1465:14
          number = Map.get(numbers_by_hashes, batch.parent_hash)

      type warning found at:
      │
 1468 │       |> Map.put(:l2_block_number, number + 1)
      │                                           ~
      │
      └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1468:43: Indexer.Fetcher.Optimism.TransactionBatch.parent_hash_to_l2_block_number/2
```

### Blockscout #26: └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1213:48: Indexer.Fetcher.Optimism.TransactionBatch.channel_complete?/1

- Message: expected a map or struct when accessing .is_last in expression:

```text
      warning: expected a map or struct when accessing .is_last in expression:

          Map.get(channel.frames, last_frame_number).is_last

      but got type:

          dynamic() or nil

      where "channel" was given the type:

          # type: dynamic(%{..., frames: map()})
          # from: lib/indexer/fetcher/optimism/transaction_batch.ex:1210:14
          Map.keys(channel.frames)

      where "last_frame_number" was given the type:

          # type: dynamic()
          # from: lib/indexer/fetcher/optimism/transaction_batch.ex:1208:23
          last_frame_number = Enum.max(Map.keys(channel.frames))

      hint: "var.field" (without parentheses) means "var" is a map() while "var.fun()" (with parentheses) means "var" is an atom()

      type warning found at:
      │
 1213 │     Map.get(channel.frames, last_frame_number).is_last and
      │                                                ~
      │
      └─ (indexer 11.0.3) lib/indexer/fetcher/optimism/transaction_batch.ex:1213:48: Indexer.Fetcher.Optimism.TransactionBatch.channel_complete?/1
```

### Blockscout #27: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/transaction_log/_logs.html.eex:48: BlockScoutWeb.TransactionLogView."_logs.html"/1

- Message: the following clause will never match:

```text
    warning: the following clause will never match:

        {:error, :no_matching_function} ->

    because it attempts to match on the result of:

        decoded_result

    which has type:

        dynamic(
          ({:ok, term(), term(), term()} and
             not {:error, :contract_not_verified, empty_list() or non_empty_list(term(), term())}) or
            {:error, :contract_not_verified, empty_list() or non_empty_list(term(), term())} or
            {:error, :could_not_decode} or {:error, :try_with_sig_provider, {term(), term()}}
        )

    type warning found at:
    │
 48 │         <% {:error, :no_matching_function} -> %>
    │         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/transaction_log/_logs.html.eex:48: BlockScoutWeb.TransactionLogView."_logs.html"/1
```

### Blockscout #28: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/transaction_log/_logs.html.eex:80:2: BlockScoutWeb.TransactionLogView."_logs.html"/1

- Message: the following clause will never match:

```text
    warning: the following clause will never match:

        {:error, :contract_verified, results} ->

    because it attempts to match on the result of:

        decoded_result

    which has type:

        dynamic(
          ({:ok, term(), term(), term()} and
             not {:error, :contract_not_verified, empty_list() or non_empty_list(term(), term())}) or
            {:error, :contract_not_verified, empty_list() or non_empty_list(term(), term())} or
            {:error, :could_not_decode} or {:error, :try_with_sig_provider, {term(), term()}}
        )

    type warning found at:
    │
 80 │           <% {:error, :contract_verified, results} -> %>
    │  ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/transaction_log/_logs.html.eex:80:2: BlockScoutWeb.TransactionLogView."_logs.html"/1
```

### Blockscout #29: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/zksync_view.ex:94:5: BlockScoutWeb.API.V2.ZkSyncView.extend_transaction_json_response/2

- Message: incompatible types given to do_add_zksync_info/2:

```text
    warning: incompatible types given to do_add_zksync_info/2:

        do_add_zksync_info(out_json, transaction)

    given types:

        dynamic(map()), -dynamic(%Explorer.Chain.Transaction{})-

    but expected one of:

        (
          map(),
          %{
            ...,
            zksync_commit_transaction: term(),
            zksync_execute_transaction: term(),
            zksync_prove_transaction: term()
          }
        )

    where "out_json" was given the types:

        # type: dynamic()
        # from: lib/block_scout_web/views/api/v2/zksync_view.ex:93:40
        out_json

        # type: dynamic(map())
        # from: lib/block_scout_web/views/api/v2/zksync_view.ex:94:5
        do_add_zksync_info(out_json, transaction)

    where "transaction" was given the type:

        # type: dynamic(%Explorer.Chain.Transaction{})
        # from: lib/block_scout_web/views/api/v2/zksync_view.ex:93:65
        %Explorer.Chain.Transaction{} = transaction

    type warning found at:
    │
 94 │     do_add_zksync_info(out_json, transaction)
    │     ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/zksync_view.ex:94:5: BlockScoutWeb.API.V2.ZkSyncView.extend_transaction_json_response/2
```

### Blockscout #30: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:43: BlockScoutWeb.AddressContractView."index.html"/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        !smart_contract_verified

    will always evaluate to true because its inner expression has type:

        dynamic(false or nil)

    type warning found at:
    │
 43 │       <%= if smart_contract_verified || (!smart_contract_verified && bytecode_twin_contract) do %>
    │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:43: BlockScoutWeb.AddressContractView."index.html"/1
```

### Blockscout #31: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/zksync_view.ex:117:5: BlockScoutWeb.API.V2.ZkSyncView.extend_block_json_response/2

- Message: incompatible types given to do_add_zksync_info/2:

```text
     warning: incompatible types given to do_add_zksync_info/2:

         do_add_zksync_info(out_json, block)

     given types:

         dynamic(map()), -dynamic(%Explorer.Chain.Block{})-

     but expected one of:

         (
           map(),
           %{
             ...,
             zksync_commit_transaction: term(),
             zksync_execute_transaction: term(),
             zksync_prove_transaction: term()
           }
         )

     where "block" was given the type:

         # type: dynamic(%Explorer.Chain.Block{})
         # from: lib/block_scout_web/views/api/v2/zksync_view.ex:116:53
         %Explorer.Chain.Block{} = block

     where "out_json" was given the types:

         # type: dynamic()
         # from: lib/block_scout_web/views/api/v2/zksync_view.ex:116:34
         out_json

         # type: dynamic(map())
         # from: lib/block_scout_web/views/api/v2/zksync_view.ex:117:5
         do_add_zksync_info(out_json, block)

     type warning found at:
     │
 117 │     do_add_zksync_info(out_json, block)
     │     ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/zksync_view.ex:117:5: BlockScoutWeb.API.V2.ZkSyncView.extend_block_json_response/2
```

### Blockscout #32: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/optimism_view.ex:403:26: BlockScoutWeb.API.V2.OptimismView.extend_block_json_response/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(block, :op_frame_sequence)

     the map:

         dynamic(%Explorer.Chain.Block{})

     does not have all required keys:

         :op_frame_sequence

     therefore this function will always return nil

     where "block" was given the type:

         # type: dynamic(%Explorer.Chain.Block{})
         # from: lib/block_scout_web/views/api/v2/optimism_view.ex:402:53
         %Explorer.Chain.Block{} = block

     type warning found at:
     │
 403 │     frame_sequence = Map.get(block, :op_frame_sequence)
     │                          ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/optimism_view.ex:403:26: BlockScoutWeb.API.V2.OptimismView.extend_block_json_response/2
```

### Blockscout #33: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:225: BlockScoutWeb.AddressContractView."index.html"/1

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         !fully_verified

     will always evaluate to true because its inner expression has type:

         dynamic(false)

     type warning found at:
     │
 225 │                   <%= if !fully_verified and !creation_code(@address) do %>
     │                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:225: BlockScoutWeb.AddressContractView."index.html"/1
```

### Blockscout #34: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/celo_view.ex:241:14: BlockScoutWeb.API.V2.CeloView.extend_address_json_response/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(
           address,
           :celo_account
         )

     the map:

         dynamic(%Explorer.Chain.Address{})

     does not have all required keys:

         :celo_account

     therefore this function will always return nil

     where "address" was given the type:

         # type: dynamic(%Explorer.Chain.Address{})
         # from: lib/block_scout_web/views/api/v2/celo_view.ex:238:57
         %Explorer.Chain.Address{} = address

     type warning found at:
     │
 241 │       |> Map.get(:celo_account)
     │              ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/celo_view.ex:241:14: BlockScoutWeb.API.V2.CeloView.extend_address_json_response/2
```

### Blockscout #35: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:612:40: BlockScoutWeb.API.V2.ArbitrumView.extend_if_message/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(arbitrum_transaction, :arbitrum_message_to_l2)

     the map:

         dynamic(%Explorer.Chain.Transaction{})

     does not have all required keys:

         :arbitrum_message_to_l2

     therefore this function will always return nil

     where "arbitrum_transaction" was given the type:

         # type: dynamic(%Explorer.Chain.Transaction{})
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:610:56
         %Explorer.Chain.Transaction{} = arbitrum_transaction

     type warning found at:
     │
 612 │       case {APIV2Helper.specified?(Map.get(arbitrum_transaction, :arbitrum_message_to_l2)),
     │                                        ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:612:40: BlockScoutWeb.API.V2.ArbitrumView.extend_if_message/2
```

### Blockscout #36: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/celo_view.ex:290:13: BlockScoutWeb.API.V2.CeloView.extend_transaction_json_response/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(transaction, :gas_token_contract_address)

     the map:

         dynamic(%Explorer.Chain.Transaction{})

     does not have all required keys:

         :gas_token_contract_address

     therefore this function will always return nil

     where "transaction" was given the type:

         # type: dynamic(%Explorer.Chain.Transaction{})
         # from: lib/block_scout_web/views/api/v2/celo_view.ex:287:65
         %Explorer.Chain.Transaction{} = transaction

     type warning found at:
     │
 290 │         Map.get(transaction, :gas_token_contract_address),
     │             ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/celo_view.ex:290:13: BlockScoutWeb.API.V2.CeloView.extend_transaction_json_response/2
```

### Blockscout #37: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:243: BlockScoutWeb.AddressContractView."index.html"/1

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         !smart_contract_verified

     will always evaluate to true because its inner expression has type:

         dynamic(false or nil)

     type warning found at:
     │
 243 │       <%= if smart_contract_verified || (!smart_contract_verified && bytecode_twin_contract) do %>
     │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract/index.html.eex:243: BlockScoutWeb.AddressContractView."index.html"/1
```

### Blockscout #38: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:688:27: BlockScoutWeb.API.V2.ArbitrumView.extend_with_transaction_info/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(arbitrum_transaction, :gas_used_for_l1)

     the map:

         dynamic(%Explorer.Chain.Transaction{})

     does not have all required keys:

         :gas_used_for_l1

     therefore this function will always return nil

     where "arbitrum_transaction" was given the type:

         # type: dynamic(%Explorer.Chain.Transaction{})
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:684:62
         %Explorer.Chain.Transaction{} = arbitrum_transaction

     type warning found at:
     │
 688 │     gas_used_for_l1 = Map.get(arbitrum_transaction, :gas_used_for_l1) || Decimal.new(0)
     │                           ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:688:27: BlockScoutWeb.API.V2.ArbitrumView.extend_with_transaction_info/2
```

### Blockscout #39: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract_verification_via_standard_json_input/new.html.eex:4: BlockScoutWeb.AddressContractVerificationViaStandardJsonInputView."new.html"/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        fetch_constructor_arguments_automatically

    will always evaluate to:

        dynamic(not false and not nil)

    where "fetch_constructor_arguments_automatically" was given the type:

        # type: dynamic(not false and not nil)
        # from: lib/block_scout_web/templates/address_contract_verification_via_standard_json_input/new.html.eex:3:46
        fetch_constructor_arguments_automatically =
          if metadata_for_verification do
            true
          else
            changeset.changes[:autodetect_constructor_args] || true
          end

    type warning found at:
    │
  4 │ <% display_constructor_arguments_text_area = if fetch_constructor_arguments_automatically, do: "none", else: "block" %>
    │ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract_verification_via_standard_json_input/new.html.eex:4: BlockScoutWeb.AddressContractVerificationViaStandardJsonInputView."new.html"/1
```

### Blockscout #40: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract_verification_via_flattened_code/new.html.eex:4: BlockScoutWeb.AddressContractVerificationViaFlattenedCodeView."new.html"/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        fetch_constructor_arguments_automatically

    will always evaluate to:

        dynamic(not false and not nil)

    where "fetch_constructor_arguments_automatically" was given the type:

        # type: dynamic(not false and not nil)
        # from: lib/block_scout_web/templates/address_contract_verification_via_flattened_code/new.html.eex:3:46
        fetch_constructor_arguments_automatically =
          if metadata_for_verification do
            true
          else
            changeset.changes[:autodetect_constructor_args] || true
          end

    type warning found at:
    │
  4 │ <% display_constructor_arguments_text_area = if fetch_constructor_arguments_automatically, do: "none", else: "block" %>
    │ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/address_contract_verification_via_flattened_code/new.html.eex:4: BlockScoutWeb.AddressContractVerificationViaFlattenedCodeView."new.html"/1
```

### Blockscout #41: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:725:39: BlockScoutWeb.API.V2.ArbitrumView.extend_with_block_info/2

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(arbitrum_block, :l1_block_number)

     the map:

         dynamic(%Explorer.Chain.Block{
           nonce: %Explorer.Chain.Hash{byte_count: integer(), bytes: bitstring()}
         })

     does not have all required keys:

         :l1_block_number

     therefore this function will always return nil

     where "arbitrum_block" was given the types:

         # type: dynamic(%Explorer.Chain.Block{})
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:722:50
         %Explorer.Chain.Block{} = arbitrum_block

         # type: dynamic(%Explorer.Chain.Block{
           nonce: %Explorer.Chain.Hash{byte_count: integer(), bytes: bitstring()}
         })
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:724:41
         Explorer.Chain.Hash.to_integer(arbitrum_block.nonce)

     type warning found at:
     │
 725 │     |> Map.put("l1_block_number", Map.get(arbitrum_block, :l1_block_number))
     │                                       ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:725:39: BlockScoutWeb.API.V2.ArbitrumView.extend_with_block_info/2
```

### Blockscout #42: └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/tokens/_tile.html.eex:12: BlockScoutWeb.TokensView."_tile.html"/1

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
    warning: the following clause cannot match because the previous clauses already matched all possible values:

        _ ->

    it attempts to match on the result of:

        foreign_token_contract_address_hash

    which has the already matched type:

        nil

    type warning found at:
    │
 12 │       <% token_hash_for_token_icon = if foreign_token_contract_address_hash, do: foreign_token_contract_address_hash, else: Address.checksum(@token.contract_address_hash) %>
    │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/templates/tokens/_tile.html.eex:12: BlockScoutWeb.TokensView."_tile.html"/1
```

### Blockscout #43: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:251:10: BlockScoutWeb.API.V2.ArbitrumView.extend_transaction_json_response/2

- Message: incompatible types given to extend_with_settlement_info/2:

```text
     warning: incompatible types given to extend_with_settlement_info/2:

         extend_with_settlement_info(
           %{},
           transaction
         )

     given types:

         empty_map(), -dynamic(%Explorer.Chain.Transaction{})-

     but expected one of:

         (
           term(),
           %{..., arbitrum_commitment_transaction: term(), arbitrum_confirmation_transaction: term()}
         )

     where "transaction" was given the type:

         # type: dynamic(%Explorer.Chain.Transaction{})
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:248:65
         %Explorer.Chain.Transaction{} = transaction

     type warning found at:
     │
 251 │       |> extend_with_settlement_info(transaction)
     │          ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:251:10: BlockScoutWeb.API.V2.ArbitrumView.extend_transaction_json_response/2
```

### Blockscout #44: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:281:10: BlockScoutWeb.API.V2.ArbitrumView.extend_block_json_response/2

- Message: incompatible types given to extend_with_settlement_info/2:

```text
     warning: incompatible types given to extend_with_settlement_info/2:

         extend_with_settlement_info(
           %{},
           block
         )

     given types:

         empty_map(), -dynamic(%Explorer.Chain.Block{})-

     but expected one of:

         (
           term(),
           %{..., arbitrum_commitment_transaction: term(), arbitrum_confirmation_transaction: term()}
         )

     where "block" was given the type:

         # type: dynamic(%Explorer.Chain.Block{})
         # from: lib/block_scout_web/views/api/v2/arbitrum_view.ex:278:53
         %Explorer.Chain.Block{} = block

     type warning found at:
     │
 281 │       |> extend_with_settlement_info(block)
     │          ~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/arbitrum_view.ex:281:10: BlockScoutWeb.API.V2.ArbitrumView.extend_block_json_response/2
```

### Blockscout #45: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/nft_helper.ex:43: BlockScoutWeb.NFTHelper.external_url/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        result

    will always evaluate to:

        dynamic(not false and not nil)

    where "result" was given the types:

        # type: dynamic()
        # from: lib/block_scout_web/views/nft_helper.ex:43:9
        result

        # type: dynamic(not false and not nil)
        # from: lib/block_scout_web/views/nft_helper.ex:43:9
        result

    type warning found at:
    │
 43 │     if !result || (result && String.trim(result)) == "", do: external_url(nil), else: result
    │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/views/nft_helper.ex:43: BlockScoutWeb.NFTHelper.external_url/1
```

### Blockscout #46: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/suave_view.ex:20:19: BlockScoutWeb.API.V2.SuaveView.extend_transaction_json_response/5

- Message: incompatible types given to Map.get/2:

```text
    warning: incompatible types given to Map.get/2:

        Map.get(transaction, :execution_node_hash)

    the map:

        dynamic(%Explorer.Chain.Transaction{})

    does not have all required keys:

        :execution_node_hash

    therefore this function will always return nil

    where "transaction" was given the type:

        # type: dynamic(%Explorer.Chain.Transaction{})
        # from: lib/block_scout_web/views/api/v2/suave_view.ex:14:24
        %Explorer.Chain.Transaction{} = transaction

    type warning found at:
    │
 20 │     if is_nil(Map.get(transaction, :execution_node_hash)) do
    │                   ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/suave_view.ex:20:19: BlockScoutWeb.API.V2.SuaveView.extend_transaction_json_response/5
```

### Blockscout #47: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/ethereum_view.ex:6:14: BlockScoutWeb.API.V2.EthereumView.extend_transaction_json_response/2

- Message: incompatible types given to Map.get/2:

```text
    warning: incompatible types given to Map.get/2:

        Map.get(transaction, :beacon_blob_transaction)

    the map:

        dynamic(%Explorer.Chain.Transaction{})

    does not have all required keys:

        :beacon_blob_transaction

    therefore this function will always return nil

    where "transaction" was given the type:

        # type: dynamic(%Explorer.Chain.Transaction{})
        # from: lib/block_scout_web/views/api/v2/ethereum_view.ex:5:65
        %Explorer.Chain.Transaction{} = transaction

    type warning found at:
    │
  6 │     case Map.get(transaction, :beacon_blob_transaction) do
    │              ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/ethereum_view.ex:6:14: BlockScoutWeb.API.V2.EthereumView.extend_transaction_json_response/2
```

### Blockscout #48: └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/ethereum_view.ex:24:25: BlockScoutWeb.API.V2.EthereumView.extend_block_json_response/3

- Message: incompatible types given to Map.get/2:

```text
    warning: incompatible types given to Map.get/2:

        Map.get(block, :blob_gas_used)

    the map:

        dynamic(%Explorer.Chain.Block{})

    does not have all required keys:

        :blob_gas_used

    therefore this function will always return nil

    where "block" was given the type:

        # type: dynamic(%Explorer.Chain.Block{})
        # from: lib/block_scout_web/views/api/v2/ethereum_view.ex:23:53
        %Explorer.Chain.Block{} = block

    type warning found at:
    │
 24 │     blob_gas_used = Map.get(block, :blob_gas_used)
    │                         ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/views/api/v2/ethereum_view.ex:24:25: BlockScoutWeb.API.V2.EthereumView.extend_block_json_response/3
```

### Blockscout #49: └─ (block_scout_web 11.0.3) lib/block_scout_web/controllers/api/health_controller.ex:61:27: BlockScoutWeb.API.HealthController.health/3

- Message: incompatible types given to Map.get/2:

```text
    warning: incompatible types given to Map.get/2:

        Map.get(Map.get(health_status, :metadata), :blocks)

    given types:

        dynamic() or nil, :blocks

    but expected one of:

        map(), term()

    where "health_status" was given the type:

        # type: dynamic(%{..., healthy: boolean()})
        # from: lib/block_scout_web/controllers/api/health_controller.ex:47:19
        health_status =
          if Application.get_env(:explorer, :chain_type) in [:arbitrum, :zksync, :optimism, :scroll] do
            batches_indexing_status = indexing_status.batches

            Map.put(
              put_in(base_health_status, [:metadata, :batches], batches_indexing_status),
              :healthy,
              indexing_status.blocks.healthy
            )
          else
            Map.put(base_health_status, :healthy, indexing_status.blocks.healthy)
          end

    type warning found at:
    │
 61 │     blocks_property = Map.get(Map.get(health_status, :metadata), :blocks)
    │                           ~
    │
    └─ (block_scout_web 11.0.3) lib/block_scout_web/controllers/api/health_controller.ex:61:27: BlockScoutWeb.API.HealthController.health/3
```

### Blockscout #50: └─ (block_scout_web 11.0.3) lib/block_scout_web/chain.ex:859: BlockScoutWeb.Chain.validate_block_number/2

- Message: the following conditional expression will always succeed:

```text
     warning: the following conditional expression will always succeed:

         validate_max_block_number?

     because it evaluates to:

         dynamic(true)

     where "validate_max_block_number?" was given the types:

         # type: dynamic(boolean())
         # from: lib/block_scout_web/chain.ex:859:8
         not validate_max_block_number?

         # type: dynamic(true)
         # from: lib/block_scout_web/chain.ex:859:8
         not validate_max_block_number?

     type warning found at:
     │
 859 │     if not validate_max_block_number? or (validate_max_block_number? and number <= BlockNumber.get_max()) do
     │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ (block_scout_web 11.0.3) lib/block_scout_web/chain.ex:859: BlockScoutWeb.Chain.validate_block_number/2
```

## Credo (6)

### Credo #1: └─ lib/credo/cli/command/diff/output/default.ex:430:14: Credo.CLI.Command.Diff.Output.Default.print_issue_trigger_marker/4

- Message: incompatible types given to String.duplicate/2:

```text
     warning: incompatible types given to String.duplicate/2:

         String.duplicate(" ", x)

     given types:

         binary(), -float()- or integer()

     but expected one of:

         binary(), integer()

     where "x" was given the type:

         # type: float() or integer()
         # from: lib/credo/cli/command/diff/output/default.ex:418:7
         x = max(issue.column - offset - 1, 0)

     type warning found at:
     │
 430 │       String.duplicate(" ", x),
     │              ~
     │
     └─ lib/credo/cli/command/diff/output/default.ex:430:14: Credo.CLI.Command.Diff.Output.Default.print_issue_trigger_marker/4
```

### Credo #2: └─ lib/credo/cli/command/suggest/output/default.ex:353:14: Credo.CLI.Command.Suggest.Output.Default.print_issue_trigger_marker/4

- Message: incompatible types given to String.duplicate/2:

```text
     warning: incompatible types given to String.duplicate/2:

         String.duplicate(" ", x)

     given types:

         binary(), -float()- or integer()

     but expected one of:

         binary(), integer()

     where "x" was given the type:

         # type: float() or integer()
         # from: lib/credo/cli/command/suggest/output/default.ex:342:7
         x = max(issue.column - offset - 1, 0)

     type warning found at:
     │
 353 │       String.duplicate(" ", x),
     │              ~
     │
     └─ lib/credo/cli/command/suggest/output/default.ex:353:14: Credo.CLI.Command.Suggest.Output.Default.print_issue_trigger_marker/4
```

### Credo #3: └─ lib/credo/code/interpolation_helper.ex:60:39: Credo.Code.InterpolationHelper.replace_line/4

- Message: incompatible types given to String.duplicate/2:

```text
    warning: incompatible types given to String.duplicate/2:

        String.duplicate(char, length)

    given types:

        binary(), -float()- or integer()

    but expected one of:

        binary(), integer()

    where "char" was given the types:

        # type: dynamic()
        # from: lib/credo/code/interpolation_helper.ex:56:47
        char

        # type: binary()
        # from: lib/credo/code/interpolation_helper.ex:60:39
        String.duplicate(char, length)

    where "length" was given the type:

        # type: float() or integer()
        # from: lib/credo/code/interpolation_helper.ex:57:12
        length = max(col_end - col_start, 0)

    type warning found at:
    │
 60 │     part2 = String.to_charlist(String.duplicate(char, length))
    │                                       ~
    │
    └─ lib/credo/code/interpolation_helper.ex:60:39: Credo.Code.InterpolationHelper.replace_line/4
```

### Credo #4: └─ lib/credo/cli/command/list/output/default.ex:152:14: Credo.CLI.Command.List.Output.Default.print_issue_column/5

- Message: incompatible types given to String.duplicate/2:

```text
     warning: incompatible types given to String.duplicate/2:

         String.duplicate(" ", x)

     given types:

         binary(), -float()- or integer()

     but expected one of:

         binary(), integer()

     where "x" was given the type:

         # type: float() or integer()
         # from: lib/credo/cli/command/list/output/default.ex:138:7
         x = max(issue.column - offset - 1, 0)

     type warning found at:
     │
 152 │       String.duplicate(" ", x),
     │              ~
     │
     └─ lib/credo/cli/command/list/output/default.ex:152:14: Credo.CLI.Command.List.Output.Default.print_issue_column/5
```

### Credo #5: └─ lib/credo/cli/output/first_run_hint.ex:15:34: Credo.CLI.Output.FirstRunHint.call/1

- Message: incompatible types given to Kernel.div/2:

```text
    warning: incompatible types given to Kernel.div/2:

        div(term_width - String.length(headline), 2)

    given types:

        -float()- or integer(), integer()

    but expected one of:

        integer(), integer()

    where "headline" was given the type:

        # type: binary()
        # from: lib/credo/cli/output/first_run_hint.ex:14:14
        headline = " 8< "

    where "term_width" was given the type:

        # type: integer()
        # from: lib/credo/cli/output/first_run_hint.ex:15:49
        term_width - String.length(headline)

    type warning found at:
    │
 15 │     bar = String.pad_leading("", div(term_width - String.length(headline), 2), "-")
    │                                  ~
    │
    └─ lib/credo/cli/output/first_run_hint.ex:15:34: Credo.CLI.Output.FirstRunHint.call/1
```

### Credo #6: └─ lib/credo/cli/command/explain/output/default.ex:506:14: Credo.CLI.Command.Explain.Output.Default.print_issue_column/4

- Message: incompatible types given to String.duplicate/2:

```text
     warning: incompatible types given to String.duplicate/2:

         String.duplicate(" ", x)

     given types:

         binary(), -float()- or integer()

     but expected one of:

         binary(), integer()

     where "x" was given the type:

         # type: float() or integer()
         # from: lib/credo/cli/command/explain/output/default.ex:492:7
         x = max(column - offset - 1, 0)

     type warning found at:
     │
 506 │       String.duplicate(" ", x),
     │              ~
     │
     └─ lib/credo/cli/command/explain/output/default.ex:506:14: Credo.CLI.Command.Explain.Output.Default.print_issue_column/4
```

## ExDoc (2)

### ExDoc #1: └─ lib/ex_doc/retriever.ex:118:9: ExDoc.Retriever.docs_chunk/1

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
     warning: the following clause cannot match because the previous clauses already matched all possible values:

         _ ->

     it attempts to match on the result of:

         result

     which has the already matched type:

         dynamic({:docs_v1, term(), term(), term(), term(), term(), term()} or {:error, term()})

     type warning found at:
     │
 118 │       _ ->
     │         ~
     │
     └─ lib/ex_doc/retriever.ex:118:9: ExDoc.Retriever.docs_chunk/1
```

### ExDoc #2: └─ lib/ex_doc/formatter/epub.ex:155:43: ExDoc.Formatter.EPUB.uuid4/0

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<:rand.uniform(4_294_967_296) - 1::integer-size(32)>>

     got type:

         float() or integer()

     but expected type:

         integer()

     type warning found at:
     │
 155 │         <<:rand.uniform(@two_power_32) - 1::32>>,
     │                                           ~
     │
     └─ lib/ex_doc/formatter/epub.ex:155:43: ExDoc.Formatter.EPUB.uuid4/0
```

## HexPm (12)

### HexPm #1: └─ lib/hexpm_web/controllers/package_controller.ex:216: HexpmWeb.PackageController.access_package/3

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         repository

     will always evaluate to:

         dynamic(not false and not nil)

     where "repository" was given the type:

         # type: dynamic(not false and not nil)
         # from: lib/hexpm_web/controllers/package_controller.ex:215:19
         repository = repositories[repository]

     type warning found at:
     │
 216 │       package = repository && Packages.get(repository, name)
     │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/hexpm_web/controllers/package_controller.ex:216: HexpmWeb.PackageController.access_package/3
```

### HexPm #2: └─ lib/hexpm_web/templates/dashboard/organization/components/billing_subscription.ex:198: HexpmWeb.Dashboard.Organization.Components.BillingSubscription."billing_subscription (overridable 1)"/1

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         !assigns.subscription

     will always evaluate to false because its inner expression has type:

         dynamic(not false and not nil)

     where "assigns" was given the types:

         # type: dynamic(
           %{..., __changed__: term(), subscription: not false and not nil} or
             %{..., subscription: not false and not nil}
         )
         # from: lib/hexpm_web/templates/dashboard/organization/components/billing_subscription.ex:41
         assigns

         # type: dynamic(%{..., subscription: term()})
         # from: lib/hexpm_web/templates/dashboard/organization/components/billing_subscription.ex:63:16
         assigns.subscription

         # type: dynamic(%{..., subscription: not false and not nil})
         # from: lib/hexpm_web/templates/dashboard/organization/components/billing_subscription.ex:63:16
         assigns.subscription

     type warning found at:
     │
 198 │               disabled={!@subscription || @subscription["cancel_at_period_end"]}
     │               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/hexpm_web/templates/dashboard/organization/components/billing_subscription.ex:198: HexpmWeb.Dashboard.Organization.Components.BillingSubscription."billing_subscription (overridable 1)"/1
```

### HexPm #3: └─ lib/hexpm_web/components/package_layout.ex:278: HexpmWeb.Components.PackageLayout."package_layout (overridable 1)"/1

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         assigns.current_release

     will always evaluate to:

         dynamic(not false and not nil)

     where "assigns" was given the types:

         # type: dynamic(
           %{..., __changed__: term(), current_release: not false and not nil} or
             %{..., current_release: not false and not nil}
         )
         # from: lib/hexpm_web/components/package_layout.ex:71
         assigns

         # type: dynamic(%{..., current_release: term()})
         # from: lib/hexpm_web/components/package_layout.ex:204:20
         assigns.current_release

         # type: dynamic(%{..., current_release: not false and not nil})
         # from: lib/hexpm_web/components/package_layout.ex:204:20
         assigns.current_release

         # type: dynamic(
           %{..., __changed__: term(), current_release: not false and not nil, graph_points: term()} or
             %{..., current_release: not false and not nil, graph_points: term()}
         )
         # from: lib/hexpm_web/components/package_layout.ex:270:24
         is_binary(assigns.graph_points)

         # type: dynamic(
           %{..., __changed__: term(), current_release: not false and not nil, graph_points: binary()} or
             %{..., current_release: not false and not nil, graph_points: binary()}
         )
         # from: lib/hexpm_web/components/package_layout.ex:270:24
         is_binary(assigns.graph_points)

     type warning found at:
     │
 278 │                         <%= if @current_release do %>
     │                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/hexpm_web/components/package_layout.ex:278: HexpmWeb.Components.PackageLayout."package_layout (overridable 1)"/1
```

### HexPm #4: └─ lib/hexpm/accounts/auth.ex:123: Hexpm.Accounts.Auth.validate_entity_auth/1

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         user

     will always evaluate to:

         dynamic(%Hexpm.Accounts.User{})

     where "user" was given the type:

         # type: dynamic(%Hexpm.Accounts.User{})
         # from: lib/hexpm/accounts/auth.ex:123:37
         %Hexpm.Accounts.User{} = user

     type warning found at:
     │
 123 │   defp validate_entity_auth(%User{} = user), do: user && not User.organization?(user)
     │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/hexpm/accounts/auth.ex:123: Hexpm.Accounts.Auth.validate_entity_auth/1
```

### HexPm #5: └─ lib/hexpm/repository/release_retirement.ex:6: HexpmWeb.Stale.Hexpm.Repository.ReleaseRetirement.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.ReleaseRetirement{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.ReleaseRetirement{})
        # from: lib/hexpm/repository/release_retirement.ex:6
        schema

    type warning found at:
    │
  6 │   embedded_schema do
    │   ~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/release_retirement.ex:6: HexpmWeb.Stale.Hexpm.Repository.ReleaseRetirement.last_modified/1
```

### HexPm #6: └─ lib/hexpm/repository/release_metadata.ex:6: HexpmWeb.Stale.Hexpm.Repository.ReleaseMetadata.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.ReleaseMetadata{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.ReleaseMetadata{})
        # from: lib/hexpm/repository/release_metadata.ex:6
        schema

    type warning found at:
    │
  6 │   embedded_schema do
    │   ~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/release_metadata.ex:6: HexpmWeb.Stale.Hexpm.Repository.ReleaseMetadata.last_modified/1
```

### HexPm #7: └─ lib/hexpm/repository/release_download.ex:7: HexpmWeb.Stale.Hexpm.Repository.ReleaseDownload.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.ReleaseDownload{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.ReleaseDownload{})
        # from: lib/hexpm/repository/release_download.ex:7
        schema

    type warning found at:
    │
  7 │   schema "release_downloads" do
    │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/release_download.ex:7: HexpmWeb.Stale.Hexpm.Repository.ReleaseDownload.last_modified/1
```

### HexPm #8: └─ lib/hexpm/repository/package_metadata.ex:6: HexpmWeb.Stale.Hexpm.Repository.PackageMetadata.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.PackageMetadata{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.PackageMetadata{})
        # from: lib/hexpm/repository/package_metadata.ex:6
        schema

    type warning found at:
    │
  6 │   embedded_schema do
    │   ~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/package_metadata.ex:6: HexpmWeb.Stale.Hexpm.Repository.PackageMetadata.last_modified/1
```

### HexPm #9: └─ lib/hexpm/repository/package_download.ex:7: HexpmWeb.Stale.Hexpm.Repository.PackageDownload.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.PackageDownload{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.PackageDownload{})
        # from: lib/hexpm/repository/package_download.ex:7
        schema

    type warning found at:
    │
  7 │   schema "package_downloads" do
    │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/package_download.ex:7: HexpmWeb.Stale.Hexpm.Repository.PackageDownload.last_modified/1
```

### HexPm #10: └─ lib/hexpm/repository/download.ex:6: HexpmWeb.Stale.Hexpm.Repository.Download.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Repository.Download{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Repository.Download{})
        # from: lib/hexpm/repository/download.ex:6
        schema

    type warning found at:
    │
  6 │   schema "downloads" do
    │   ~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/repository/download.ex:6: HexpmWeb.Stale.Hexpm.Repository.Download.last_modified/1
```

### HexPm #11: └─ lib/hexpm/accounts/key_permission.ex:8: HexpmWeb.Stale.Hexpm.Accounts.KeyPermission.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Accounts.KeyPermission{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Accounts.KeyPermission{})
        # from: lib/hexpm/accounts/key_permission.ex:8
        schema

    type warning found at:
    │
  8 │   embedded_schema do
    │   ~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/accounts/key_permission.ex:8: HexpmWeb.Stale.Hexpm.Accounts.KeyPermission.last_modified/1
```

### HexPm #12: └─ lib/hexpm/accounts/user_handles.ex:6: HexpmWeb.Stale.Hexpm.Accounts.UserHandles.last_modified/1

- Message: incompatible types given to Map.fetch!/2:

```text
    warning: incompatible types given to Map.fetch!/2:

        Map.fetch!(schema, :updated_at)

    the map:

        dynamic(%Hexpm.Accounts.UserHandles{})

    does not have all required keys:

        :updated_at

    therefore this function will always raise

    where "schema" (context HexpmWeb.Stale.Any) was given the type:

        # type: dynamic(%Hexpm.Accounts.UserHandles{})
        # from: lib/hexpm/accounts/user_handles.ex:6
        schema

    type warning found at:
    │
  6 │   embedded_schema do
    │   ~~~~~~~~~~~~~~~~~~
    │
    └─ lib/hexpm/accounts/user_handles.ex:6: HexpmWeb.Stale.Hexpm.Accounts.UserHandles.last_modified/1
```

## Livebook (6)

### Livebook #1: └─ lib/livebook_web/live/session_live/k8s_runtime_component.ex:793: LivebookWeb.SessionLive.K8sRuntimeComponent.kubectl_warning/0

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
     warning: the following clause cannot match because the previous clauses already matched all possible values:

         _ ->

     it attempts to match on the result of:

         Livebook.Config.app?()

     which has the already matched type:

         dynamic(false)

     type warning found at:
     │
 793 │       if Livebook.Config.app?() do
     │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/livebook_web/live/session_live/k8s_runtime_component.ex:793: LivebookWeb.SessionLive.K8sRuntimeComponent.kubectl_warning/0
```

### Livebook #2: └─ lib/livebook_web/components/layouts/root.html.heex:17: LivebookWeb.Layouts.root/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        dev?()

    will always evaluate to:

        dynamic(true)

    type warning found at:
    │
 17 │     <%= if dev?() do %>
    │     ~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/livebook_web/components/layouts/root.html.heex:17: LivebookWeb.Layouts.root/1
```

### Livebook #3: └─ lib/livebook_web/controllers/error_html.ex:63: LivebookWeb.ErrorHTML."error_page (overridable 1)"/1

- Message: the following conditional expression:

```text
    warning: the following conditional expression:

        LivebookWeb.Layouts.dev?()

    will always evaluate to:

        dynamic(true)

    type warning found at:
    │
 63 │         <%= if LivebookWeb.Layouts.dev?() do %>
    │         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/livebook_web/controllers/error_html.ex:63: LivebookWeb.ErrorHTML."error_page (overridable 1)"/1
```

### Livebook #4: └─ lib/livebook_web/controllers/auth_html/index.html.heex:15: LivebookWeb.AuthHTML.index/1

- Message: the following clause cannot match because the previous clauses already matched all possible values:

```text
    warning: the following clause cannot match because the previous clauses already matched all possible values:

        _ ->

    it attempts to match on the result of:

        Livebook.Config.app?()

    which has the already matched type:

        dynamic(false)

    type warning found at:
    │
 15 │         <%= if Livebook.Config.app?() do %>
    │         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/livebook_web/controllers/auth_html/index.html.heex:15: LivebookWeb.AuthHTML.index/1
```

### Livebook #5: └─ lib/livebook_web/helpers/codec_helpers.ex:72:21: LivebookWeb.CodecHelpers.encode_pcm_as_wav_header/3

- Message: incompatible types in binary construction:

```text
    warning: incompatible types in binary construction:

        <<..., 36 + data_size::integer-little-unsigned-size(32), ...>>

    got type:

        float() or integer()

    but expected type:

        integer()

    where "data_size" was given the type:

        # type: float() or integer()
        # from: lib/livebook_web/helpers/codec_helpers.ex:68:15
        data_size = num_frames * block_align

    type warning found at:
    │
 72 │       36 + data_size::32-unsigned-integer-little,
    │                     ~
    │
    └─ lib/livebook_web/helpers/codec_helpers.ex:72:21: LivebookWeb.CodecHelpers.encode_pcm_as_wav_header/3
```

### Livebook #6: └─ lib/livebook/live_markdown/markdown_helpers.ex:364:21: Livebook.LiveMarkdown.MarkdownHelpers.pad_whitespace/2

- Message: incompatible types given to String.duplicate/2:

```text
     warning: incompatible types given to String.duplicate/2:

         String.duplicate(" ", missing)

     given types:

         binary(), -float()- or integer()

     but expected one of:

         binary(), integer()

     where "missing" was given the type:

         # type: float() or integer()
         # from: lib/livebook/live_markdown/markdown_helpers.ex:363:15
         missing = max(width - length, 0)

     type warning found at:
     │
 364 │       [cell, String.duplicate(" ", missing)]
     │                     ~
     │
     └─ lib/livebook/live_markdown/markdown_helpers.ex:364:21: Livebook.LiveMarkdown.MarkdownHelpers.pad_whitespace/2
```

## MixSBOM (2)

### MixSBOM #1: └─ lib/sbom/cyclonedx/common/enum_helpers.ex:155: SBoM.CycloneDX.Common.EnumHelpers.classification_to_string_xml/1

- Message: the right-hand side of || will never be executed:

```text
     warning: the right-hand side of || will never be executed:

         classification_to_string(type) || ...

     because the left-hand side always evaluates to:

         binary()

     where "type" was given the type:

         # type: dynamic(not :CLASSIFICATION_NULL)
         # from: lib/sbom/cyclonedx/common/enum_helpers.ex:155:36
         type

     type warning found at:
     │
 155 │   def classification_to_string_xml(type), do: classification_to_string(type) || ""
     │   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/sbom/cyclonedx/common/enum_helpers.ex:155: SBoM.CycloneDX.Common.EnumHelpers.classification_to_string_xml/1
```

### MixSBOM #2: └─ lib/sbom/fetcher/mix_runtime.ex:143: SBoM.Fetcher.MixRuntime.resolve_dep/3

- Message: the following conditional expression:

```text
     warning: the following conditional expression:

         load_from_app_spec?

     will always evaluate to:

         dynamic(true)

     where "load_from_app_spec?" was given the type:

         # type: dynamic(true)
         # from: lib/sbom/fetcher/mix_runtime.ex:139:27
         load_from_app_spec? =
           not (
             {arg1} = {app}

             arg1 === :eex or arg1 === :elixir or arg1 === :ex_unit or arg1 === :iex or arg1 === :logger or
               arg1 === :mix or
               (arg1 === :stdlib or arg1 === :common_test or arg1 === :runtime_tools or arg1 === :sasl or
                  arg1 === :ftp or arg1 === :eldap or arg1 === :dialyzer or arg1 === :megaco or
                  arg1 === :eunit or arg1 === :wx or arg1 === :edoc or arg1 === :syntax_tools or
                  arg1 === :crypto or arg1 === :debugger or arg1 === :asn1 or arg1 === :compiler or
                  arg1 === :et or arg1 === :mnesia or arg1 === :inets or arg1 === :reltool or
                  arg1 === :tools or arg1 === :os_mon or arg1 === :diameter or arg1 === :snmp or
                  arg1 === :observer or arg1 === :parsetools or arg1 === :erl_interface or
                  arg1 === :public_key or arg1 === :erts or arg1 === :kernel or arg1 === :tftp or
                  arg1 === :odbc or arg1 === :xmerl or arg1 === :ssh or arg1 === :ssl) or arg1 == :hex
           ) or not in_burrito?()

     type warning found at:
     │
 143 │           if load_from_app_spec? do
     │           ~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/sbom/fetcher/mix_runtime.ex:143: SBoM.Fetcher.MixRuntime.resolve_dep/3
```

## OpenApiSpex (7)

### OpenApiSpex #1: └─ lib/open_api_spex/operation.ex:319:12: OpenApiSpex.Operation.validate_body_schema/4

- Message: incompatible types given to Map.get/2:

```text
     warning: incompatible types given to Map.get/2:

         Map.get(
           Map.get(
             content,
             content_type
           ),
           :schema
         )

     given types:

         dynamic() or nil, :schema

     but expected one of:

         map(), term()

     where "content" was given the type:

         # type: dynamic(map())
         # from: lib/open_api_spex/operation.ex:318:12
         Map.get(
           content,
           content_type
         )

     where "content_type" was given the type:

         # type: dynamic()
         # from: lib/open_api_spex/operation.ex:316:69
         content_type

     type warning found at:
     │
 319 │     |> Map.get(:schema)
     │            ~
     │
     └─ lib/open_api_spex/operation.ex:319:12: OpenApiSpex.Operation.validate_body_schema/4
```

### OpenApiSpex #2: └─ lib/open_api_spex/operation2.ex:57:14: OpenApiSpex.Operation2.cast_conn/2

- Message: incompatible types given to Map.get/3:

```text
    warning: incompatible types given to Map.get/3:

        Map.get(
          Map.get(
            conn,
            :private
          ),
          :open_api_spex,
          %{}
        )

    given types:

        dynamic() or nil, :open_api_spex, empty_map()

    but expected one of:

        map(), term(), term()

    where "conn" was given the type:

        # type: dynamic(map())
        # from: lib/open_api_spex/operation2.ex:56:14
        Map.get(
          conn,
          :private
        )

    type warning found at:
    │
 57 │       |> Map.get(:open_api_spex, %{})
    │              ~
    │
    └─ lib/open_api_spex/operation2.ex:57:14: OpenApiSpex.Operation2.cast_conn/2
```

### OpenApiSpex #3: └─ lib/open_api_spex/plug/put_api_spec.ex:33:14: OpenApiSpex.Plug.PutApiSpec.call/2

- Message: incompatible types given to Map.get/3:

```text
    warning: incompatible types given to Map.get/3:

        Map.get(
          Map.get(
            conn,
            :private
          ),
          :open_api_spex,
          %{}
        )

    given types:

        dynamic() or nil, :open_api_spex, empty_map()

    but expected one of:

        map(), term(), term()

    where "conn" was given the type:

        # type: dynamic(map())
        # from: lib/open_api_spex/plug/put_api_spec.ex:32:14
        Map.get(
          conn,
          :private
        )

    type warning found at:
    │
 33 │       |> Map.get(:open_api_spex, %{})
    │              ~
    │
    └─ lib/open_api_spex/plug/put_api_spec.ex:33:14: OpenApiSpex.Plug.PutApiSpec.call/2
```

### OpenApiSpex #4: └─ lib/open_api_spex/cast_parameters.ex:21:14: OpenApiSpex.CastParameters.cast_conn/2

- Message: incompatible types given to Map.get/3:

```text
    warning: incompatible types given to Map.get/3:

        Map.get(
          Map.get(
            conn,
            :private
          ),
          :open_api_spex,
          %{}
        )

    given types:

        dynamic() or nil, :open_api_spex, empty_map()

    but expected one of:

        map(), term(), term()

    where "conn" was given the type:

        # type: dynamic(map())
        # from: lib/open_api_spex/cast_parameters.ex:20:14
        Map.get(
          conn,
          :private
        )

    type warning found at:
    │
 21 │       |> Map.get(:open_api_spex, %{})
    │              ~
    │
    └─ lib/open_api_spex/cast_parameters.ex:21:14: OpenApiSpex.CastParameters.cast_conn/2
```

### OpenApiSpex #5: └─ lib/open_api_spex/controller.ex:184: OpenApiSpex.Controller.__api_operation__/2

- Message: the right-hand side of || will never be executed:

```text
     warning: the right-hand side of || will never be executed:

         description || ...

     because the left-hand side always evaluates to:

         dynamic(not false and not nil)

     where "description" was given the type:

         # type: dynamic(not false and not nil)
         # from: lib/open_api_spex/controller.ex
         {:ok, {mod_meta, summary, description, meta}}

     type warning found at:
     │
 184 │           description: description || "",
     │           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/open_api_spex/controller.ex:184: OpenApiSpex.Controller.__api_operation__/2
```

### OpenApiSpex #6: └─ lib/mix/tasks/openapi.spec.yaml.ex:57: Mix.Tasks.Openapi.Spec.Yaml.encoder/0

- Message: the right-hand side of || will never be executed:

```text
    warning: the right-hand side of || will never be executed:

        OpenApiSpex.OpenApi.yaml_encoder() || ...

    because the left-hand side always evaluates to:

        dynamic(OpenApiSpex.OpenApi.YmlrEncoder)

    type warning found at:
    │
 57 │     OpenApiSpex.OpenApi.yaml_encoder() ||
    │     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    │
    └─ lib/mix/tasks/openapi.spec.yaml.ex:57: Mix.Tasks.Openapi.Spec.Yaml.encoder/0
```

### OpenApiSpex #7: └─ lib/open_api_spex/plug/cast_and_validate.ex:159:14: OpenApiSpex.Plug.CastAndValidate.put_operation_id/2

- Message: incompatible types given to Map.get/3:

```text
     warning: incompatible types given to Map.get/3:

         Map.get(
           Map.get(
             conn,
             :private
           ),
           :open_api_spex,
           %{}
         )

     given types:

         dynamic() or nil, :open_api_spex, empty_map()

     but expected one of:

         map(), term(), term()

     where "conn" was given the type:

         # type: dynamic(map())
         # from: lib/open_api_spex/plug/cast_and_validate.ex:158:14
         Map.get(
           conn,
           :private
         )

     type warning found at:
     │
 159 │       |> Map.get(:open_api_spex, %{})
     │              ~
     │
     └─ lib/open_api_spex/plug/cast_and_validate.ex:159:14: OpenApiSpex.Plug.CastAndValidate.put_operation_id/2
```

## PhoenixLiveView (1)

### PhoenixLiveView #1: └─ lib/phoenix_live_view/html_formatter.ex:613:10: Phoenix.LiveView.HTMLFormatter.line_byte_offset/3

- Message: incompatible types given to Kernel.binary_part/3:

```text
     warning: incompatible types given to Kernel.binary_part/3:

         binary_part(source, line_offset, byte_size(source) - line_offset)

     given types:

         binary(), -float()- or integer(), -float()- or integer()

     but expected one of:

         binary(), integer(), integer()

     where "line_offset" was given the type:

         # type: float() or integer()
         # from: lib/phoenix_live_view/html_formatter.ex:609:17
         line_offset = line_before + line_size

     where "source" was given the types:

         # type: dynamic()
         # from: lib/phoenix_live_view/html_formatter.ex:608:25
         source

         # type: binary()
         # from: lib/phoenix_live_view/html_formatter.ex:613:10
         binary_part(source, line_offset, byte_size(source) - line_offset)

     type warning found at:
     │
 613 │       |> binary_part(line_offset, byte_size(source) - line_offset)
     │          ~
     │
     └─ lib/phoenix_live_view/html_formatter.ex:613:10: Phoenix.LiveView.HTMLFormatter.line_byte_offset/3
```

## SQL (11)

### SQL #1: └─ lib/bnf.ex:11:18: SQL.BNF.parse/0

- Message: incompatible types given as default arguments to parse/1:

```text
    warning: incompatible types given as default arguments to parse/1:

        -empty_map()-

    but expected one of:

        %{..., download: true} or %{..., path: term()} or binary()

    type warning found at:
    │
 11 │   def parse(opts \\ %{}) do
    │                  ~
    │
    └─ lib/bnf.ex:11:18: SQL.BNF.parse/0
```

### SQL #2: └─ lib/adapters/postgres.ex:368:19: SQL.Adapters.Postgres.bind/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., bind_len::integer-big-size(32), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "bind_len" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:367:14
         bind_len = 12 + len + byte_size(name) + (idx + c_len) * 2 + byte_size(params_bin)

     type warning found at:
     │
 368 │     <<?B, bind_len::32-big, portal::binary, 0, name::binary, 0, idx::16-big, formats(idx)::binary, idx::16-big, params_bin::binary, c_len::16-big, formats(c_len)::binary,?E,len+9::32,portal::binary,0,0::32-big,?C,len+6::32,?P,portal::binary,0,?H,4::32-big>>
     │                   ~
     │
     └─ lib/adapters/postgres.ex:368:19: SQL.Adapters.Postgres.bind/2
```

### SQL #3: └─ lib/adapters/postgres.ex:374:19: SQL.Adapters.Postgres.bind/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., bind_len::integer-big-size(32), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "bind_len" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:373:14
         bind_len = 12 + len + byte_size(name) + (idx + c_len) * 2 + byte_size(params_bin)

     type warning found at:
     │
 374 │     <<?B, bind_len::32-big, portal::binary, 0, name::binary, 0, idx::16-big, formats(idx)::binary, idx::16-big, params_bin::binary, c_len::16-big, formats(c_len)::binary,?E,len+9::32,portal::binary,0,0::32-big,?C,len+6::32,?P,portal::binary,0,?H,4::32-big>>
     │                   ~
     │
     └─ lib/adapters/postgres.ex:374:19: SQL.Adapters.Postgres.bind/2
```

### SQL #4: └─ lib/adapters/postgres.ex:380:19: SQL.Adapters.Postgres.bind/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., bind_len::integer-big-size(32), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "bind_len" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:379:14
         bind_len = 12 + len + byte_size(name) + (idx + c_len) * 2 + byte_size(params_bin)

     type warning found at:
     │
 380 │     <<?B, bind_len::32-big, portal::binary, 0, name::binary, 0, idx::16-big, formats(idx)::binary, idx::16-big, params_bin::binary, c_len::16-big, formats(c_len)::binary,?E,len+9::32,portal::binary,0,max_rows::32-big,?H,4::32-big>>
     │                   ~
     │
     └─ lib/adapters/postgres.ex:380:19: SQL.Adapters.Postgres.bind/2
```

### SQL #5: └─ lib/adapters/postgres.ex:706:21: SQL.Adapters.Postgres.encode/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., us::integer-big-signed-size(64), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "us" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:705:8
         us = 1_000_000 * (3600 * hour + 60 * minute + second) + microsecond

     type warning found at:
     │
 706 │     <<16::32-big, us::64-signed-big, days::32-signed-big, months::32-signed-big>>
     │                     ~
     │
     └─ lib/adapters/postgres.ex:706:21: SQL.Adapters.Postgres.encode/2
```

### SQL #6: └─ lib/adapters/postgres.ex:729:21: SQL.Adapters.Postgres.encode/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., ms::integer-big-signed-size(64), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "ms" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:728:8
         ms = seconds * 1_000_000 + ms

     type warning found at:
     │
 729 │     <<12::32-big, ms::signed-64-big, 0::signed-32-big>>
     │                     ~
     │
     └─ lib/adapters/postgres.ex:729:21: SQL.Adapters.Postgres.encode/2
```

### SQL #7: └─ lib/adapters/postgres.ex:749:89: SQL.Adapters.Postgres.encode/2

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., Date.to_gregorian_days(date) - 730_485::integer-big-signed-size(32)>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "date" was given the types:

         # type: dynamic(%Date{})
         # from: lib/adapters/postgres.ex:749:29
         %Date{} = date

         # type: dynamic(
           %Date{calendar: atom() and not Calendar.ISO} or
             %Date{year: integer(), month: integer(), day: integer(), calendar: Calendar.ISO}
         )
         # from: lib/adapters/postgres.ex:749:59
         Date.to_gregorian_days(date)

     type warning found at:
     │
 749 │   defp encode(:date, %Date{}=date), do: <<4::32-big, Date.to_gregorian_days(date)-730485::signed-32-big>>
     │                                                                                         ~
     │
     └─ lib/adapters/postgres.ex:749:89: SQL.Adapters.Postgres.encode/2
```

### SQL #8: └─ lib/adapters/postgres.ex:794:19: SQL.Adapters.Postgres.encode_numeric/8

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<10 + count::integer-big-size(32), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "count" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:793:15
         count = count + 1

     type warning found at:
     │
 794 │         <<10+count::32-big, count::16-big, weight::16-big, sign::16-big, 0::16-big, bin::binary, group::16>>
     │                   ~
     │
     └─ lib/adapters/postgres.ex:794:19: SQL.Adapters.Postgres.encode_numeric/8
```

### SQL #9: └─ lib/adapters/postgres.ex:803:19: SQL.Adapters.Postgres.encode_numeric/8

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<10 + count::integer-big-size(32), ...>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "count" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:802:15
         count = count + 1

     type warning found at:
     │
 803 │         <<10+count::32-big, count::16-big, weight-1::16-big, sign::16-big, scale+1::16-big, bin::binary, group::16>>
     │                   ~
     │
     └─ lib/adapters/postgres.ex:803:19: SQL.Adapters.Postgres.encode_numeric/8
```

### SQL #10: └─ lib/adapters/postgres.ex:812:98: SQL.Adapters.Postgres.encode_numeric/8

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., group * 10 + digit::integer-size(16)>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "digit" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:810:11
         digit = n - 48

     where "group" was given the type:

         # type: integer()
         # from: lib/adapters/postgres.ex:812:89
         group * 10

     type warning found at:
     │
 812 │       4 -> encode_numeric(rest, sign, weight, scale, 0, 0, count+1, <<bin::binary, group*10+digit::16>>)
     │                                                                                                  ~
     │
     └─ lib/adapters/postgres.ex:812:98: SQL.Adapters.Postgres.encode_numeric/8
```

### SQL #11: └─ lib/adapters/postgres.ex:819:100: SQL.Adapters.Postgres.encode_numeric/8

- Message: incompatible types in binary construction:

```text
     warning: incompatible types in binary construction:

         <<..., group * 10 + digit::integer-size(16)>>

     got type:

         float() or integer()

     but expected type:

         integer()

     where "digit" was given the type:

         # type: float() or integer()
         # from: lib/adapters/postgres.ex:817:11
         digit = n - 48

     where "group" was given the type:

         # type: integer()
         # from: lib/adapters/postgres.ex:819:91
         group * 10

     type warning found at:
     │
 819 │       4 -> encode_numeric(rest, sign, weight, scale+1, 0, 0, count+1, <<bin::binary, group*10+digit::16>>)
     │                                                                                                    ~
     │
     └─ lib/adapters/postgres.ex:819:100: SQL.Adapters.Postgres.encode_numeric/8
```

## Spitfire (2)

### Spitfire #1: └─ lib/spitfire/tracer.ex:30:23: Spitfire.Tracer.stop_trace/1

- Message: incompatible types given to String.duplicate/2:

```text
    warning: incompatible types given to String.duplicate/2:

        String.duplicate(" ", indent() * 2)

    given types:

        binary(), -float()- or integer()

    but expected one of:

        binary(), integer()

    type warning found at:
    │
 30 │     IO.puts("#{String.duplicate(" ", indent() * 2)}END: #{name}")
    │                       ~
    │
    └─ lib/spitfire/tracer.ex:30:23: Spitfire.Tracer.stop_trace/1
```

### Spitfire #2: └─ lib/spitfire/env.ex:220: Spitfire.Env.expand/3

- Message: the following conditional expression will always succeed:

```text
     warning: the following conditional expression will always succeed:

         is_atom(arg)

     because it evaluates to:

         true

     where "arg" was given the type:

         # type: dynamic(atom())
         # from: lib/spitfire/env.ex:218:8
         is_atom(arg)

     type warning found at:
     │
 220 │       with true <- is_atom(arg) and Code.ensure_loaded?(arg),
     │       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     │
     └─ lib/spitfire/env.ex:220: Spitfire.Env.expand/3
```
