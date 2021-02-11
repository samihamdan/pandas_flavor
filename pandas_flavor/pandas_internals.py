from pandas.core.groupby.generic import DataFrameGroupBy
try:
    # Import register decorators from pandas >= 0.23
    from pandas.api.extensions import (register_dataframe_accessor,
                                       register_series_accessor)

    # Register groupby >= 0.23
    try:
        # >= 1.0
        from pandas.util._decorators import doc
        from pandas.core.accessor import _register_accessor

        @doc(_register_accessor, klass="DataFrameGroupBy")
        def register_groupby_accessor(name):
            """Register custom accessor on DataFrameGroupBy."""

            return _register_accessor(name, DataFrameGroupBy)

    except ImportError:
        try:
            # 0.23 <= Pandas > 1.0
            from pandas.core.accessor import _doc, _register_accessor
            from pandas.util._decorators import Appender

            @Appender(
                _doc
                % dict(
                    klass="DataFrame", others=(
                        "register_groupby_accessor, register_index_accessor")
                )
            )
            def register_groupby_accessor(name):
                """Register custom accessor on DataFrameGroupBy."""

                return _register_accessor(name, DataFrameGroupBy)

except ImportError:
    from pandas import DataFrame, Series

    try:
        from pandas.core.accessor import AccessorProperty
    except ImportError:  # Pandas before 0.22.0
        from pandas.core.base import AccessorProperty

    # Define register decorators for pandas < 0.23
    class register_dataframe_accessor(object):
        """Register custom accessor on DataFrame."""

        def __init__(self, name):
            self.name = name

        def __call__(self, accessor):
            setattr(DataFrame, self.name, AccessorProperty(accessor, accessor))

    class register_series_accessor(object):
        """Register custom accessor on Series."""

        def __init__(self, name):
            self.name = name

        def __call__(self, accessor):
            setattr(Series, self.name, AccessorProperty(accessor, accessor))

    class register_groupby_accessor(object):
        """Register custom accessor on DataFrameGroupBy."""

        def __init__(self, name):
            self.name = name

        def __call__(self, accessor):
            setattr(DataFrameGroupBy, self.name,
                    AccessorProperty(accessor, accessor))
