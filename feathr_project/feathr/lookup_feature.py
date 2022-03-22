from copy import copy, deepcopy
from typing import List, Optional, Union

from jinja2 import Template

from feathr.dtype import FeatureType
from feathr.feature import FeatureBase
from feathr.transformation import RowTransformation
from feathr.typed_key import DUMMY_KEY, TypedKey
from feathr.aggregation import Aggregation

class LookupFeature(FeatureBase):
    """A lookup feature is a feature defined on top of two other features, i.e. using the feature value 
    of the base feature as key, to lookup the feature value from the expansion feature.
    Attributes:
        name: Derived feature name
        feature_type: Type of derived feature
        key: Join key of the derived feature
        base_feature: The feature value of this feature will be used as key to lookup from the expansion feature
        expansion_feature: The feature to be lookup
        aggregation: Specify the aggregation for the feature values lookup from the expansion feature, in the
                     case of the base feature value needed to be converted into multiple lookup keys, 
                     e.g. feature value is an array and each value in the array is used once as a lookup key.   
    """

    def __init__(self,
                name: str,
                feature_type: FeatureType,
                base_feature: FeatureBase,
                expansion_feature: FeatureBase,
                aggregation: Aggregation,
                key: Optional[Union[TypedKey, List[TypedKey]]] = [DUMMY_KEY]):
        super(LookupFeature, self).__init__(name, feature_type, key=key)
        self.base_feature = base_feature
        self.expansion_feature = expansion_feature
        self.aggregation = aggregation

    def to_feature_config(self) -> str:
        tm = Template("""
            {{lookup_feature.name}}: {
                key: [{{','.join(lookup_feature.key_alias)}}]
                join: {
                    base:{ 
                            key: [{{','.join(lookup_feature.base_feature.key_alias)}}],
                            feature: {{lookup_feature.base_feature.name}} 
                         }
                    expansion: { 
                            key: [{{','.join(lookup_feature.expansion_feature.key_alias)}}],
                            feature: {{lookup_feature.expansion_feature.name}}
                         } 
                }
                aggregation: {{lookup_feature.aggregation.name}}
                {{lookup_feature.feature_type.to_feature_config()}}
            }
        """)
        return tm.render(lookup_feature=self)