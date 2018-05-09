import 'normalize.css';
import Turbolinks from 'turbolinks';

import closeButton from './closeButton';
import onload from './onload';

Turbolinks.start();

onload(closeButton);
