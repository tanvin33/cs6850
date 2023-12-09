from new_model import self_testing_model_constant
import numpy as np
import plotly.graph_objects as go  # install with pip install plotly

if __name__ == "__main__":
    Zt = 1500
    Zc = 30
    k = 2  # time at which contact tracing begins

    result = np.zeros((11, 11, 11))

    for p in range(0, 11):
        for q in range(0, 11):
            for r in range(0, 11):
                num_contained = 0
                # G, color_map, return_code = self_testing_model_constant(p/10.0, q/10.0, r/10.0, Zc, Zt, k)
                # return_code = np.random.randint(1, 4)
                for i in range(10):
                    G, color_map, return_code = self_testing_model_constant(
                        p / 10.0, q / 10.0, r / 10.0, Zc, Zt, k
                    )
                    if return_code == 2:
                        num_contained += 1
                result[p, q, r] = num_contained / 10.0
                # result[p, q, r] = return_code

    X, Y, Z = np.mgrid[0:11, 0:11, 0:11]  # axis values

    fig = go.Figure(
        data=go.Volume(
            x=(X / 10).flatten(),
            y=(Y / 10).flatten(),
            z=(Z / 10).flatten(),
            value=result.flatten(),
            opacity=0.1,
            surface_count=17,
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis={"autorange": "reversed"},
            xaxis_title="p",
            yaxis_title="q",
            zaxis_title="r",
        )
    )  # label axis
    fig.write_html("probabilities.html")
    fig.show()
