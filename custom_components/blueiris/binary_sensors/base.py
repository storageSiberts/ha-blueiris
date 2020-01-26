"""
Support for Blue Iris binary sensors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.blueiris/
"""
import logging

from homeassistant.components.binary_sensor import (BinarySensorDevice)

from custom_components.blueiris.const import *

_LOGGER = logging.getLogger(__name__)


class BlueIrisBinarySensor(BinarySensorDevice):
    """Representation a binary sensor that is updated by MQTT."""

    def __init__(self, camera, sensor_type_name):
        """Initialize the MQTT binary sensor."""
        super().__init__()

        camera_id = camera.get(CONF_ID)
        camera_name = camera.get(CONF_NAME)

        state_topic = MQTT_ALL_TOPIC.replace('+', camera_id)

        device_class = SENSOR_DEVICE_CLASS.get(sensor_type_name, sensor_type_name).lower()

        self._name = f"{camera_name} {sensor_type_name}"
        self._state = False
        self._state_topic = state_topic
        self._device_class = device_class
        self._event_type = sensor_type_name.lower()

    def update_data(self, event_type, trigger):
        _LOGGER.info(f"Handling {self._name} {event_type} event with value: {trigger}")

        self._state = trigger == STATE_ON

        self.async_schedule_update_ha_state()

    @property
    def topic(self):
        """Return the polling state."""
        return self._state_topic

    @property
    def event_type(self):
        """Return the polling state."""
        return self._event_type

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._name

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def force_update(self):
        """Force update."""
        return DEFAULT_FORCE_UPDATE
