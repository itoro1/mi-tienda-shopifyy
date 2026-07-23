import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

// Placeholder reveal: fade + rise, eased with `spring` (never linear — see
// SKILL.md "Easing"). Replace with the slot's actual composition; keep the
// same non-linear easing discipline for anything you add.
export const Main: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const progress = spring({
		frame,
		fps,
		config: {damping: 200},
	});

	const opacity = interpolate(progress, [0, 1], [0, 1]);
	const translateY = interpolate(progress, [0, 1], [20, 0]);

	return (
		<AbsoluteFill
			style={{
				backgroundColor: '#0a0a0a',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<div
				style={{
					opacity,
					transform: `translateY(${translateY}px)`,
					color: '#ffffff',
					fontFamily: 'Helvetica, Arial, sans-serif',
					fontSize: 64,
					fontWeight: 700,
				}}
			>
				Edit me
			</div>
		</AbsoluteFill>
	);
};
