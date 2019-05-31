#係り受け解析プログラム
import CaboCha

#token.surface = 形態素解析文字, token.chunk = NULLもある,
#token->chunk->link,かかり先ID
# token->chunk->head_pos,主辞
#  token->chunk->func_pos,機能語
#   token->chunk->scoreスコア
#feature, 詞や読みなど形態素の情報部分

def get_word(tree, chunk):
    surface = ''
    for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
        token = tree.token(i)
        features = token.feature.split(',')

        #名詞, 形容動詞, 形容詞, 動詞のみの係り受けを抽出
        if features[0] == '名詞':
            surface += token.surface
        elif features[0] == '形容詞':
            surface += features[6]
            break
        elif features[0] == '動詞':
            surface += features[6]
            break
        elif features[0] == '形容動詞':
            surface += features[6]
            break
    return surface

def get_2_words(line):

    cp = CaboCha.Parser('-f1')
    #木構造を作成
    tree = cp.parse(line)

    chunk_dic = {}
    chunk_id = 0

    for i in range(0, tree.size()):
        token = tree.token(i)

        if token.chunk:
            #形態素ごとにchunk丸ごと辞書型に格納
            #link, head_pos, func_pos, score
            chunk_dic[chunk_id] = token.chunk
            #chank_id = chank_link
            chunk_id += 1

    tuples = []
    for chunk_id, chunk in chunk_dic.items():

         #係り受けが存在したら
        if chunk.link > 0:
            from_surface =  get_word(tree, chunk)
            to_chunk = chunk_dic[chunk.link]
            to_surface = get_word(tree, to_chunk)
            tuples.append((from_surface, to_surface))

    return tuples


if __name__ == '__main__' :


    #line = 'このホテルはとても綺麗です。'
    line = input("文章は？")
    line = line.split("。")

    #文章ごとに係り受け解析
    for i in range(len(line) - 1):
        tuples = get_2_words(line[i])

    for t in tuples:
        if t[0] != '' and t[1] != '':
            print(t[0] + ' => ' + t[1])



#
