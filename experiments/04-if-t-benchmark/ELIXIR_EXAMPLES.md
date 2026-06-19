# Core Elixir If-T Examples

This file shows the Elixir code for the thirteen core If-T benchmark examples
used by Experiment 04. The source is reconstructed from the archived benchmark
patch series, corresponding to `Elixir/main.ex` on the
`elixir-narrowing-benchmark` branch.

```elixir
### Code:
## Example positive
## success
defmodule IfTBenchmarkElixir.PositiveSuccess do
  @assert_type_form (term() -> term())
  def f(x) do
    if is_binary(x) do
      byte_size(x)
    else
      x
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.PositiveFailure do
  @assert_type_form (term() -> term())
  def f(x) do
    if is_binary(x) do
      x + 1
    else
      x
    end
  end
end

## Example negative
## success
defmodule IfTBenchmarkElixir.NegativeSuccess do
  @assert_type_form (binary() or integer() -> integer())
  def f(x) do
    if is_binary(x) do
      byte_size(x)
    else
      x + 1
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.NegativeFailure do
  @assert_type_form (binary() or integer() or boolean() -> integer())
  def f(x) do
    if is_binary(x) do
      byte_size(x)
    else
      x + 1
    end
  end
end

## Example connectives
## success
defmodule IfTBenchmarkElixir.ConnectivesSuccess do
  @assert_type_form (binary() or integer() -> integer())
  def f(x) do
    if not is_integer(x), do: byte_size(x), else: 0
  end

  @assert_type_form (term() -> integer())
  def g(x) when is_binary(x) or is_integer(x), do: f(x)
  def g(_x), do: 0

  @assert_type_form (binary() or integer() or boolean() -> integer())
  def h(x) do
    if not is_boolean(x) and not is_integer(x), do: byte_size(x), else: 0
  end
end

## failure
## subcase f
defmodule IfTBenchmarkElixir.ConnectivesFailure do
  @assert_type_form (binary() or integer() -> integer())
  def f(x) do
    if not is_integer(x), do: x + 1, else: 0
  end
end

## subcase g
defmodule IfTBenchmarkElixir.ConnectivesFailure do
  @assert_type_form (term() -> integer())
  def g(x) when is_binary(x) or is_integer(x), do: x + 1
  def g(_x), do: 0
end

## subcase h
defmodule IfTBenchmarkElixir.ConnectivesFailure do
  @assert_type_form (binary() or integer() or boolean() -> integer())
  def h(x) do
    if not is_boolean(x) and not is_integer(x), do: x + 1, else: 0
  end
end

## Example nesting_body
## success
defmodule IfTBenchmarkElixir.NestingBodySuccess do
  @assert_type_form (binary() or integer() or boolean() -> integer())
  def f(x) do
    if not is_binary(x) do
      if not is_boolean(x) do
        x + 1
      else
        0
      end
    else
      0
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.NestingBodyFailure do
  @assert_type_form (binary() or integer() or boolean() -> integer())
  def f(x) do
    if is_binary(x) or is_integer(x) do
      if is_integer(x) or is_boolean(x) do
        byte_size(x)
      else
        0
      end
    else
      0
    end
  end
end

## Example struct_fields
## success
defmodule IfTBenchmarkElixir.StructFieldsSuccess do
  @assert_type_form (%{..., a: term()} -> integer())
  def f(x) do
    if is_integer(x.a) do
      x.a
    else
      0
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.StructFieldsFailure do
  @assert_type_form (%{..., a: term()} -> integer())
  def f(x) do
    if is_binary(x.a) do
      x.a
    else
      0
    end
  end
end

## Example tuple_elements
## success
defmodule IfTBenchmarkElixir.TupleElementsSuccess do
  @assert_type_form ({term(), term()} -> integer())
  def f(x) do
    if is_integer(elem(x, 0)) do
      elem(x, 0)
    else
      0
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.TupleElementsFailure do
  @assert_type_form ({term(), term()} -> integer())
  def f(x) do
    if is_integer(elem(x, 0)) do
      elem(x, 0) + elem(x, 1)
    else
      0
    end
  end
end

## Example tuple_length
## success
defmodule IfTBenchmarkElixir.TupleLengthSuccess do
  @define_type_form int_pair: {integer(), integer()}
  @define_type_form string_triple: {binary(), binary(), binary()}
  @assert_type_form (int_pair() or string_triple() -> integer())
  def f(x) do
    if tuple_size(x) == 2 do
      elem(x, 0) + elem(x, 1)
    else
      byte_size(elem(x, 0))
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.TupleLengthFailure do
  @define_type_form int_pair: {integer(), integer()}
  @define_type_form string_triple: {binary(), binary(), binary()}
  @assert_type_form (int_pair() or string_triple() -> integer())
  def f(x) do
    if tuple_size(x) == 2 do
      elem(x, 0) + elem(x, 1)
    else
      elem(x, 0) + elem(x, 1)
    end
  end
end

## Example alias
## success
defmodule IfTBenchmarkElixir.AliasSuccess do
  @assert_type_form (term() -> term())
  def f(x) do
    y = is_binary(x)

    if y do
      byte_size(x)
    else
      x
    end
  end
end

## failure
## subcase saved-alias
defmodule IfTBenchmarkElixir.AliasFailure do
  @assert_type_form (term() -> term())
  def f(x) do
    y = is_binary(x)

    if y do
      x + 1
    else
      x
    end
  end
end

## subcase reassigned-alias
defmodule IfTBenchmarkElixir.AliasFailure do
  @assert_type_form (term() -> term())
  def g(x) do
    y = is_binary(x)
    y = true

    if y do
      byte_size(x)
    else
      x
    end
  end
end

## Example nesting_condition
## success
defmodule IfTBenchmarkElixir.NestingConditionSuccess do
  @assert_type_form (term(), term() -> integer())
  def f(x, y) do
    if if(is_integer(x), do: is_binary(y), else: false) do
      x + byte_size(y)
    else
      0
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.NestingConditionFailure do
  @assert_type_form (term(), term() -> integer())
  def f(x, y) do
    if if(is_integer(x), do: is_binary(y), else: is_binary(y)) do
      x + byte_size(y)
    else
      0
    end
  end
end

## Example merge_with_union
## success
defmodule IfTBenchmarkElixir.MergeWithUnionSuccess do
  @assert_type_form (term() -> binary() or integer())
  def f(x) do
    x =
      if is_binary(x) do
        x <> "hello"
      else
        if is_integer(x) do
          x + 1
        else
          0
        end
      end

    x
  end
end

## failure
defmodule IfTBenchmarkElixir.MergeWithUnionFailure do
  @assert_type_form (term() -> binary() or integer())
  def f(x) do
    x =
      if is_binary(x) do
        x <> "hello"
      else
        if is_integer(x) do
          x + 1
        else
          0
        end
      end

    x + 1
  end
end

## Example predicate_2way
## success
defmodule IfTBenchmarkElixir.Predicate2WaySuccess do
  @assert_type_form (binary() -> true) and (integer() -> false)
  def helper(x), do: is_binary(x)

  @assert_type_form (binary() or integer() -> integer())
  def g(x) do
    if helper(x) do
      byte_size(x)
    else
      x
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.Predicate2WayFailure do
  @assert_type_form (binary() -> true) and (integer() -> false)
  def helper(x), do: is_binary(x)

  @assert_type_form (binary() or integer() -> integer())
  def g(x) do
    if helper(x) do
      x + 1
    else
      x
    end
  end
end

## Example predicate_1way
## success
defmodule IfTBenchmarkElixir.Predicate1WaySuccess do
  @assert_type_form (integer() -> boolean()) and (binary() -> false)
  def helper(x) when is_integer(x), do: x > 0
  def helper(x) when is_binary(x), do: false

  @assert_type_form (binary() or integer() -> integer())
  def g(x) do
    if helper(x) do
      x + 1
    else
      0
    end
  end
end

## failure
defmodule IfTBenchmarkElixir.Predicate1WayFailure do
  @assert_type_form (integer() -> boolean()) and (binary() -> false)
  def helper(x) when is_integer(x), do: x > 0
  def helper(x) when is_binary(x), do: false

  @assert_type_form (binary() or integer() -> integer())
  def g(x) do
    if helper(x) do
      x + 1
    else
      byte_size(x)
    end
  end
end

## Example predicate_checked
## success
defmodule IfTBenchmarkElixir.PredicateCheckedSuccess do
  @assert_type_form (binary() -> true) and (integer() or boolean() -> false)
  def helper(x), do: is_binary(x)

  @assert_type_form (binary() -> false) and (integer() or boolean() -> true)
  def g(x), do: not helper(x)
end

## failure
## subcase f
defmodule IfTBenchmarkElixir.PredicateCheckedFailure do
  @assert_type_form (binary() -> true) and (integer() or boolean() -> false)
  def f(x), do: is_binary(x) or is_integer(x)
end

## subcase g
defmodule IfTBenchmarkElixir.PredicateCheckedFailure do
  @assert_type_form (binary() -> false) and (integer() or boolean() -> true)
  def g(x), do: is_integer(x)
end
```
