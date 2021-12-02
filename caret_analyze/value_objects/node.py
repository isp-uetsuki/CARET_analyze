# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Optional, Tuple

from ..exceptions import ItemNotFoundError
from ..common import Util
from .callback_group import CallbackGroupStructValue
from .callback import CallbackStructValue
from .node_path import NodePathStructValue
from .publisher import PublisherStructValue
from .subscription import SubscriptionStructValue
from .value_object import ValueObject
from .variable_passing import VariablePassingStructValue
from .message_context import MessageContext


class NodeValue(ValueObject):
    def __init__(
        self,
        node_name: str,
        node_id: Optional[str],
    ) -> None:
        self.__node_name = node_name
        self.__node_id = node_id

    @property
    def node_name(self) -> str:
        return self.__node_name

    @property
    def node_id(self) -> Optional[str]:
        return self.__node_id


class NodeStructValue(ValueObject):
    """Executor info for architecture."""

    def __init__(
        self,
        node_name: str,
        publisher_values: Tuple[PublisherStructValue, ...],
        subscriptions_info: Tuple[SubscriptionStructValue, ...],
        node_path_values: Tuple[NodePathStructValue, ...],
        callback_group_values: Optional[Tuple[CallbackGroupStructValue, ...]],
        variable_passing_values: Optional[Tuple[VariablePassingStructValue, ...]],
        message_contexts: Tuple[MessageContext, ...]
    ) -> None:
        self._node_name = node_name
        self._publishers = publisher_values
        self._subscriptions = subscriptions_info
        self._callback_groups = callback_group_values
        self._node_path_values = node_path_values
        self._variable_passings_info = variable_passing_values
        self._message_contexts = message_contexts

    @property
    def node_name(self) -> str:
        return self._node_name

    @property
    def publisher(self) -> Tuple[PublisherStructValue, ...]:
        return self._publishers

    @property
    def publish_topic_names(self) -> Tuple[str, ...]:
        return tuple(p.topic_name for p in self._publishers)

    @property
    def subscribe_topic_names(self) -> Tuple[str, ...]:
        return tuple(s.topic_name for s in self._subscriptions)

    @property
    def subscription_values(self) -> Tuple[SubscriptionStructValue, ...]:
        return self._subscriptions

    @property
    def callbacks(self) -> Optional[Tuple[CallbackStructValue, ...]]:
        if self._callback_groups is None:
            return None
        return tuple(Util.flatten(cbg.callbacks for cbg in self._callback_groups))

    @property
    def callback_names(self) -> Optional[Tuple[str, ...]]:
        if self.callbacks is None:
            return None
        return tuple(_.callback_name for _ in self.callbacks)

    @property
    def callback_groups(self) -> Optional[Tuple[CallbackGroupStructValue, ...]]:
        return self._callback_groups

    @property
    def callback_group_names(self) -> Optional[Tuple[str, ...]]:
        if self.callback_groups is None:
            return None
        return tuple(_.callback_group_name for _ in self.callback_groups)

    @property
    def paths(self) -> Tuple[NodePathStructValue, ...]:
        return self._node_path_values

    @property
    def variable_passings(self) -> Optional[Tuple[VariablePassingStructValue, ...]]:
        return self._variable_passings_info

    @property
    def message_contexts(self) -> Tuple[MessageContext, ...]:
        return self._message_contexts

    def get_subscription(
        self,
        subscribe_topic_name: str
    ) -> SubscriptionStructValue:

        try:
            return Util.find_one(
                lambda x: x.topic_name == subscribe_topic_name,
                self._subscriptions)
        except ItemNotFoundError:
            msg = 'Failed to find subscription info. '
            msg += f'topic_name: {subscribe_topic_name}'
            raise ItemNotFoundError(msg)

    def get_publisher(
        self,
        publish_topic_name: str
    ) -> PublisherStructValue:
        try:
            return Util.find_one(
                lambda x: x.topic_name == publish_topic_name,
                self._publishers)
        except ItemNotFoundError:
            msg = 'Failed to find publisher info. '
            msg += f'topic_name: {publish_topic_name}'
            raise ItemNotFoundError(msg)
