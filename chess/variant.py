# -*- coding: utf-8 -*-
#
# This file is part of the python-chess library.
# Copyright (C) 2016 Niklas Fiekas <niklas.fiekas@backscattering.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import chess


SUICIDE_STARTING_FEN = chess.STARTING_FEN

class SuicideBoard(chess.Board):

    uci_variant = "suicide"
    starting_fen = SUICIDE_STARTING_FEN

    tbw_suffix = ".stbw"
    tbz_suffix = ".stbz"
    tbw_magic = [0x7b, 0xf6, 0x93, 0x15]
    tbz_magic = [0xe4, 0xcf, 0xe7, 0x23]
    connected_kings = True
    one_king = False

    def pin_mask(self, color, square):
        return chess.BB_ALL

    def _attacked_for_king(self, path):
        return False

    def _ep_skewered(self, capturer_mask):
        return False

    def is_check(self):
        return False

    def is_into_check(self, move):
        return False

    def was_into_check(self, move):
        return False

    def _material_balance(self):
        return (chess.pop_count(self.occupied_co[self.turn]) -
                chess.pop_count(self.occupied_co[not self.turn]))

    def is_variant_win(self):
        if not self.occupied_co[self.turn]:
            return True
        else:
            return self.is_stalemate() and self._material_balance() < 0

    def is_variant_loss(self):
        if not self.occupied_co[self.turn]:
            return False
        else:
            return self.is_stalemate() and self._material_balance() > 0

    def is_variant_draw(self):
        if not self.occupied_co[self.turn]:
            return False
        else:
            return self.is_stalemate() and self._material_balance() == 0

    def is_insufficient_material(self):
        # Enough material.
        if self.knights or self.rooks or self.queens or self.kings:
            return False

        # Must have bishops.
        if not (self.occupied_co[chess.WHITE] & self.bishops and self.occupied_co[chess.BLACK] & self.bishops):
            return False

        # All pawns must be blocked.
        w_pawns = self.pawns & self.occupied_co[chess.WHITE]
        b_pawns = self.pawns & self.occupied_co[chess.BLACK]

        b_blocked_pawns = chess.shift_up(w_pawns) & b_pawns
        w_blocked_pawns = chess.shift_down(b_pawns) & w_pawns

        if (b_blocked_pawns | w_blocked_pawns) != self.pawns:
            return False

        turn = self.turn
        turn = chess.WHITE
        if any(self.generate_pseudo_legal_moves(self.pawns)):
            return False
        turn = chess.BLACK
        if any(self.generate_pseudo_legal_moves(self.pawns)):
            return False
        self.turn = turn

        # Bishop and pawns of each side are on distinct color complexes.
        if self.occupied_co[chess.WHITE] & chess.BB_DARK_SQUARES == 0:
            return self.occupied_co[chess.BLACK] & chess.BB_LIGHT_SQUARES == 0
        elif self.occupied_co[chess.WHITE] & chess.BB_LIGHT_SQUARES == 0:
            return self.occupied_co[chess.BLACK] & chess.BB_DARK_SQUARES == 0
        else:
            return False

    def generate_pseudo_legal_moves(self, from_mask=chess.BB_ALL, to_mask=chess.BB_ALL):
        for move in super(SuicideBoard, self).generate_pseudo_legal_moves(from_mask, to_mask):
            # Add king promotions.
            if move.promotion == chess.QUEEN:
                yield chess.Move(move.from_square, move.to_square, chess.KING)

            yield move

    def generate_evasions(self, from_mask=chess.BB_ALL, to_mask=chess.BB_ALL):
        return
        yield

    def generate_non_evasions(self, from_mask=chess.BB_ALL, to_mask=chess.BB_ALL):
        # Generate captures first.
        found_capture = False
        for move in self.generate_pseudo_legal_captures():
            if chess.BB_SQUARES[move.from_square] & from_mask and chess.BB_SQUARES[move.to_square] & to_mask:
                yield move
            found_capture = True

        # Captures are mandatory. Stop here if any were found.
        if not found_capture:
            not_them = to_mask & ~self.occupied_co[not self.turn]
            for move in self.generate_pseudo_legal_moves(from_mask, not_them):
                if not self.is_en_passant(move):
                    yield move

    def status(self):
        status = super(SuicideBoard, self).status()
        status &= ~chess.STATUS_NO_WHITE_KING
        status &= ~chess.STATUS_NO_BLACK_KING
        status &= ~chess.STATUS_TOO_MANY_KINGS
        status &= ~chess.STATUS_OPPOSITE_CHECK
        return status


GIVEAWAY_STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"

class GiveawayBoard(SuicideBoard):

    uci_variant = "giveaway"
    starting_fen = GIVEAWAY_STARTING_FEN

    tbw_suffix = ".gtbw"
    tbz_suffix = ".gtbz"
    tbw_magic = [0xBC, 0x55, 0xBC, 0x21]
    tbz_magic = [0xD6, 0xF5, 0x1B, 0x50]

    def __init__(self, fen=GIVEAWAY_STARTING_FEN, chess960=False):
        super(GiveawayBoard, self).__init__(fen, chess960)

        # Give back castling rights that were removed when resetting.
        if fen == chess.STARTING_FEN:
            self.castling_rights = chess.BB_A1 | chess.BB_H1 | chess.BB_A8 | chess.BB_H8

    def reset(self):
        super(GiveawayBoard, self).reset()
        self.castling_rights = chess.BB_VOID

    def is_variant_win(self):
        return not self.occupied_co[self.turn] or self.is_stalemate()

    def is_variant_loss(self):
        return False

    def is_variant_draw(self):
        return False


ATOMIC_STARTING_FEN = chess.STARTING_FEN

class AtomicBoard(chess.Board):

    uci_variant = "atomic"
    starting_fen = ATOMIC_STARTING_FEN

    tbw_suffix = ".atbw"
    tbz_suffix = ".atbz"
    tbw_magic = [0x55, 0x8D, 0xA4, 0x49]
    tbz_magic = [0x91, 0xA9, 0x5E, 0xEB]
    connected_kings = True
    one_king = True

    def is_variant_win(self):
        return not self.kings & self.occupied_co[not self.turn]

    def is_variant_loss(self):
        return not self.kings & self.occupied_co[self.turn]

    def is_insufficient_material(self):
        if self.is_variant_loss() or self.is_variant_win():
            return False

        if self.pawns or self.queens:
            return False

        if chess.pop_count(self.KNIGHT | self.BISHOP | self.ROOK) == 1:
            return True

        # Only knights.
        if self.occupied == (self.kings | self.knights):
            return chess.pop_count(self.knights) <= 2

        # Only bishops.
        if self.occupied == (self.kings | self.bishops):
            # All bishops on opposite colors.
            if not self.pieces_mask(chess.BISHOP, chess.WHITE) & chess.BB_DARK_SQUARES:
                return not self.pieces_mask(chess.BISHOP, chess.BLACK) & chess.BB_LIGHT_SQUARES
            if not self.pieces_mask(chess.BISHOP, chess.WHITE) & chess.BB_LIGHT_SQUARES:
                return not self.pieces_mask(chess.BISHOP, chess.BLACK) & chess.BB_DARK_SQUARES

        return False

    def _attacked_for_king(self, path):
        # Can castle onto attacked squares if they are connected to the
        # enemy king.
        enemy_kings = self.kings & self.occupied_co[not self.turn]
        enemy_king = chess.bit_scan(enemy_kings)
        while enemy_king != -1 and enemy_king is not None:
            path &= ~chess.BB_KING_ATTACKS[enemy_king]
            enemy_king = chess.bit_scan(enemy_kings, enemy_king + 1)

        return super(AtomicBoard, self)._attacked_for_king(path)

    def _kings_connected(self):
        kings = self.kings & self.occupied_co[chess.WHITE]
        king_square = chess.bit_scan(kings)
        while king_square != -1 and king_square is not None:
            if chess.BB_KING_ATTACKS[king_square] & self.kings & self.occupied_co[chess.BLACK]:
                return True

            king_square = chess.bit_scan(kings, king_square + 1)

        return False

    def _push_capture(self, move, capture_square, piece_type):
        # Explode the capturing piece.
        self._remove_piece_at(move.to_square)

        # Explode all non pawns around.
        explosion_radius = chess.BB_KING_ATTACKS[capture_square] & ~self.pawns
        explosion = chess.bit_scan(explosion_radius)
        while explosion != -1 and explosion is not None:
            self._remove_piece_at(explosion)
            explosion = chess.bit_scan(explosion_radius, explosion + 1)

    def is_check(self):
        return not self.is_variant_loss() and not self._kings_connected() and super(AtomicBoard, self).is_check()

    def was_into_check(self):
        return not self.is_variant_win() and not self._kings_connected() and super(AtomicBoard, self).was_into_check()

    def is_into_check(self, move):
        self.push(move)
        was_into_check = self.was_into_check()
        self.pop()
        return was_into_check

    def is_stalemate(self):
        return not self.is_variant_loss() and super(AtomicBoard, self).is_stalemate()

    def generate_legal_moves(self, from_mask=chess.BB_ALL, to_mask=chess.BB_ALL):
        if self.is_variant_loss():
            return

        for move in self.generate_pseudo_legal_moves(from_mask, to_mask):
            if not self.is_into_check(move):
                yield move

    generate_evasions = generate_non_evasions = generate_legal_moves

    def status(self):
        status = super(SuicideBoard, self).status()
        status &= ~chess.STATUS_OPPOSITE_CHECK
        if self.turn == chess.WHITE:
            status &= ~chess.STATUS_NO_WHITE_KING
        else:
            status &= ~chess.STATUS_NO_BLACK_KING
        return status


BB_HILL = chess.BB_E4 | chess.BB_D4 | chess.BB_E5 | chess.BB_D5

KING_OF_THE_HILL_STARTING_FEN = chess.STARTING_FEN

class KingOfTheHillBoard(chess.Board):

    uci_variant = "kingofthehill"

    tbw_suffix = tbz_suffix = None
    tbw_magic = tbz_magic = None

    def is_variant_win(self):
        return self.kings & self.occupied_co[self.turn] & BB_HILL

    def is_variant_loss(self):
        return self.kings & self.occupied_co[not self.turn] & BB_HILL

    def is_insufficient_material(self):
        return False


# TODO: Crazyhouse
# TODO: Racing kings
# TODO: Horde
