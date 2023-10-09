#!/bin/bash
set -e

export APP=device-management

# We need to know if flavor is set
if [ ! -z ${FLAVOR+x} ] ; then
  echo "* Starting APP=${APP} with FLAVOR=${FLAVOR}"
else
  echo "* WARNING: No FLAVOR, environment may not load properly."
fi

if [[ ${CHAMBER_ENABLED:-true} == false ]]; then
  echo "* CHAMBER_ENABLED is ${CHAMBER_ENABLED@Q} so skipping attempt to load environment via chamber"
else
  chamber_environments="global $FLAVOR $APP ${FLAVOR:+$APP-$FLAVOR}"
  echo "* Attempting to load environment variables from SSM parameter store via chamber. Environments: $chamber_environments"
  source <(chamber -r 3 exec $chamber_environments -- sh -c 'export -p')
fi

if [[ $1 =~ ^(/bin/)?(ba)?sh$ ]]; then
  echo "* First CMD argument is a shell: $1"
  echo "* Running: exec ${@@Q}"
  exec "$@"
elif [[ "$*" =~ ([;<>]|\(|\)|\&\&|\|\|) ]]; then
  echo "* Shell metacharacters detected, passing CMD to bash"
  _quoted="$*"
  echo "* Running: exec /bin/bash -c ${_quoted@Q}"
  unset _quoted
  exec /bin/bash -c "$*"
fi

# Use dumb-init to ensure proper handling of signals, zombies, etc.
# See https://github.com/Yelp/dumb-init

echo "* Running command: /usr/local/bin/dumb-init ${@@Q}"
exec /usr/local/bin/dumb-init "$@"
