import {Composition} from 'remotion';
import {Main} from './Main';

// Defaults match a common video-use overlay target (1080p@30, 5s).
// Edit fps/width/height/durationInFrames per the slot's actual spec —
// keep it in sync with the EDL overlay entry and verify with ffprobe
// after rendering.
export const Root: React.FC = () => {
	return (
		<Composition
			id="Main"
			component={Main}
			durationInFrames={150}
			fps={30}
			width={1920}
			height={1080}
		/>
	);
};
